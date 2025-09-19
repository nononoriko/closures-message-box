from telegram import Bot, InputMediaPhoto
from datetime import datetime, timezone, timedelta
import json, tweepy, asyncio

with open("./main/data.json") as file:
    dataDict = json.load(file)

def get_recent_tweets(client: tweepy.Client) -> tweepy.client.Response:
    now = datetime.now(timezone.utc)
    startTime = now - timedelta(days=1)
    
    user = client.get_user(username=dataDict["AccountHandle"])
    userID = user.data.id

    tweets = client.get_users_tweets(
        id=userID,
        start_time = to_rfc3339(startTime),
        end_time = to_rfc3339(now),
        max_results = 5,
        tweet_fields = ["created_at"],
        expansions = ["attachments.media_keys"],
        media_fields=["url", "preview_image_url", "type"]
    )

    return tweets

def to_rfc3339(dt: datetime):
    dt.astimezone(timezone.utc)
    ms = int(dt.microsecond / 1000)

    return dt.strftime(f"%Y-%m-%dT%H:%M:%S.{ms:03d}Z")

def extract_tweet_data(tweets):
    results = []
    media_lookup = {}

    if "media" in tweets.includes:
        for media in tweets.includes["media"]:
            media_lookup[media.media_key] = media
    
    for tweet in tweets.data:
        text = tweet.text
        urls = []

        if hasattr(tweet, "attachments") and "media_keys" in tweet.attachments:
            for key in tweet.attachments["media_keys"]:
                if key in media_lookup:
                    media = media_lookup[key]
                    if media.type == "photo":
                        urls.append(media.url)
                    elif media.type in ["video", "animated_gif"]:
                        urls.append(media.preview_image_url)
                        has_video = True
        results.append(
            {
                "text": text, 
                "media": urls, 
                "id": tweet.id,
                "has_video": has_video,
                "created_at": tweet.created_at.strftime("%Y-%m-%d %H:%M:%S UTC")
            }
        )

    return results

async def main():
    TBot = Bot(dataDict["BotToken"])
    client = tweepy.Client(
        bearer_token=dataDict["XToken"],
        wait_on_rate_limit=True
    )

    tweets = get_recent_tweets(client)
    extracted = extract_tweet_data(tweets)

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

if __name__ == "__main__":
    asyncio.run(main())