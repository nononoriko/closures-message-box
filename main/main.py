from telegram import Bot, InputMediaPhoto
from datetime import datetime, timezone, timedelta
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from urllib.parse import urlparse
import json, tweepy, asyncio, argparse

parser = argparse.ArgumentParser(
    description="Command line arguments for Closure's Message Box."
)

parser.add_argument(
    "maxResult",
    type=int,
    nargs="?",
    default=0,
    help="Limit the amount of posts to pull. No limit by default."
)

parser.add_argument(
    "hour",
    type=int,
    nargs="?",
    default=9,
    help="Hour of the day (0–23) when the script should run. Default: 9. Will be ignore if --inf isn't provided."
)

parser.add_argument(
    "minute",
    type=int,
    nargs="?",
    default=0,
    help="Minute of the hour (0–59) when the script should run. Default: 0. Will be ignore if --inf isn't provided."
)

parser.add_argument(
    "--inf",
    action="store_true",
    default=False,
    help="Whether to run the script indefinitely until interrupt by the user. Run once by default."
)

cl_args = parser.parse_args()

requiredKeys = ["XToken", "BotToken", "AccountHandle", "ChatID"]

with open("./main/data.json") as file:
    dataDict = json.load(file)
    missingKeys = [key for key in requiredKeys if key not in dataDict]
    if missingKeys:
        print(f"Missing {", ".join(missingKeys)} from data.json, cannot continue, exiting.")
        exit(-1)

def get_recent_tweets(client: tweepy.Client) -> tweepy.client.Response:
    now = datetime.now(timezone.utc)
    startTime = now - timedelta(days=1)
    
    user = client.get_user(username=dataDict["AccountHandle"])
    userID = user.data.id

    kwargs = {
        "id": userID,
        "start_time": to_rfc3339(startTime),
        "end_time": to_rfc3339(now),
        "tweet_fields": ["created_at", "entities"],
        "expansions": ["attachments.media_keys"],
        "media_fields": ["url", "preview_image_url", "type"]
    }

    if cl_args.maxResult > 0:
        kwargs["max_results"] = cl_args.maxResult

    tweets = client.get_users_tweets(**kwargs)

    return tweets

def to_rfc3339(dt: datetime) -> str:
    dt.astimezone(timezone.utc)
    ms = int(dt.microsecond / 1000)

    return dt.strftime(f"%Y-%m-%dT%H:%M:%S.{ms:03d}Z")

def is_url(url: str) -> bool:
    try:
        urlparse(url)
        return True
    except:
        return False

def extract_tweet_data(tweets, timezone) -> list[dict]:
    results = []
    media_lookup = {}

    if "media" in tweets.includes:
        for m in tweets.includes["media"]:
            media_lookup[m.media_key] = m

    for tweet in tweets.data:
        text = tweet.text
        urls_to_replace = []

        if tweet.entities and "urls" in tweet.entities:
            for url_entity in tweet.entities["urls"]:
                tco = url_entity["url"] if isinstance(url_entity, dict) else url_entity.url
                expanded = url_entity["expanded_url"] if isinstance(url_entity, dict) else url_entity.expanded_url

                is_media_url = any(
                    getattr(m, "url", None) and m.url in tco
                    for m in media_lookup.values()
                )
                if not is_media_url:
                    urls_to_replace.append((tco, expanded))

        for tco, expanded in urls_to_replace:
            text = text.replace(tco, expanded)

        if tweet.entities and "mentions" in tweet.entities:
            for mention in tweet.entities["mentions"]:
                username = mention["username"] if isinstance(mention, dict) else mention.username
                text = text.replace(f"@{username}", f"https://x.com/{username}")

        lines:list[str] = text.strip().splitlines()
        try:
            last_line = lines.pop()

            for chars in last_line.split(" "):
                if(is_url(chars)):
                    parsed_url = urlparse(chars)
                    if parsed_url.netloc == "x.com" and ("photo" in parsed_url.path or "video" in parsed_url.path):
                        last_line = last_line.replace(chars, "")
            
            lines.append(last_line)
        except:
            ...

        text = "\n".join(lines)

        urls = []
        has_video = False
        if tweet.attachments and "media_keys" in tweet.attachments:
            for key in tweet.attachments["media_keys"]:
                if key in media_lookup:
                    media = media_lookup[key]
                    if media.type == "photo":
                        urls.append(media.url)
                    elif media.type in ["video", "animated_gif"]:
                        urls.append(media.preview_image_url)
                        has_video = True

        local_time = tweet.created_at.astimezone(timezone)
        time_str = local_time.strftime("%Y-%m-%d %H:%M:%S %Z")

        results.append(
            {
                "id": tweet.id,
                "text": text,
                "media": urls,
                "has_video": has_video,
                "created_at": time_str,
            }
        )

    return results

def clamp(number: int | float, min: int | float, max: int | float = None) -> int | float:
    if max is None:
        max, min = min, 0

    return max if number > max else min if number < min else number

async def main(timezone) -> None:
    TBot = Bot(dataDict["BotToken"])
    client = tweepy.Client(
        bearer_token=dataDict["XToken"],
        wait_on_rate_limit=True
    )

    tweets = get_recent_tweets(client)
    extracted = extract_tweet_data(tweets, timezone)

    for tweet in extracted:
        caption = f"""{tweet["text"]}

[Timestamp] {tweet["created_at"]}
[Link] https://x.com/{dataDict["AccountHandle"]}/status/{tweet["id"]}
[Video] {"Yes" if tweet["has_video"] else "No"}"""
        if tweet["media"]:
            mediaGroup = []

            for i, img in enumerate(tweet["media"]):
                if i == 0:
                    mediaGroup.append(InputMediaPhoto(img, caption))
                else:
                    mediaGroup.append(InputMediaPhoto(img))
                
            await TBot.send_media_group(dataDict["ChatID"], mediaGroup)
        else:
            await TBot.send_message(dataDict["ChatID"], caption)

async def run(timezone):
    main(timezone)

async def run_scheduler(timezone):
    scheduler = AsyncIOScheduler(timezone=timezone)
    run_hour = clamp(cl_args.hour, 23)
    run_minute = clamp(cl_args.minute, 59)

    scheduler.add_job(
        run,
        "cron",
        hour=run_hour,
        minute=run_minute,
        args=[timezone]
    )
    scheduler.start()

    try:
        asyncio.Event().wait()
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()

if __name__ == "__main__":
    localTimeZone = datetime.now().astimezone().tzinfo

    if cl_args.inf:
        asyncio.run(run_scheduler(localTimeZone))
    else:
        asyncio.run(run(localTimeZone))