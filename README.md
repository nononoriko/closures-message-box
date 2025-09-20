# Closure's Message Box
A Telegram bot that periodically updates you with ~~Tweets~~ Xs, from your favorite ~~Twitter~~ X account from the last 24 hours.

## Prerequisites
1. [Python](https://www.python.org/downloads/) (Preferably the newest version)
2. [python-telegram-bot](https://pypi.org/project/python-telegram-bot/) (Ditto, install after Python)
   ```bash
   pip install python-telegram-bot
   ```
3. [tweepy](https://pypi.org/project/tweepy/) (Ditto)
   ```bash
   pip install tweepy
   ```
4. [apscheduler](https://pypi.org/project/APScheduler/) (Ditto)
   ```bash
   pip install apscheduler
   ```
   Alternatively, you can use Windows' Task Scheduler instead, though modification to the ```main.py``` file is required.
5. A [~~Twitter~~ X](https://developer.x.com/en/portal/products) API Bearer Token. (Do not share this with anyone unless you know what you're doing)
6. A [Telegram Bot](https://t.me/BotFather) token. (Ditto)
7. The handle(username) of your desired ~~Twitter~~ X account.
8. The ID of the chat you want the bot to send updates to.

## Running
1. Clone this repository (Requires [Git](https://git-scm.com/downloads)):
   ```bash
   git clone https://github.com/uwungu01-rep/closures-message-box
   ```
   Alternatively, download the [zip](https://github.com/uwungu01-rep/closures-message-box/archive/refs/heads/main.zip) file and unzip it at your desired location.
2. Create a file named data.json in the ```main``` folder. The file should look something like this:
   ```json
   {
      "XToken": "YOUR_TWITTER_API_TOKEN",
      "BotToken": "YOUR_TELEGRAM_BOT_TOKEN",
      "AccountHandle": "THE_HANDLE(USERNAME_WITHOUT_THE_@)_OF_THE_ACCOUNT_YOU_WANT_TO_TRACK",
      "ChatID": "THE_ID_OF_THE_CHAT_YOU_WANT_THE_BOT_TO_SEND_UPDATES"
   }
   ```
3. Run ```closures-message-box.bat``` in the ```run``` folder. Optionally with [arguments](#command-line-arguments).
4. And you're done.

## Command line arguments
1. maxResult: Limit the amount of post the script will pull. No limit by default.
2. hour: Hour of the day (0–23) when the script should run. Default: 9. Will be ignore if --inf isn't provided.
3. minute: Minute of the hour (0–59) when the script should run. Default: 0. Will be ignore if --inf isn't provided.
4. --inf: Whether to run the script indefinitely until interrupt by the user. Run once by default.

## Note(s)
1. This script was design to work with ~~Twitter~~ X's free API. Higher tiers require additional adjustments if you want the bot to send videos.
2. Running this with a smaller interval and on different accounts is theoretically possible, but you need to make adjustments to the source and be prepared to be rate-limited by Elon Musk unless you're using higher tiers.

## License
This program is licensed under the GNU General Public License 3.0, see [LICENSE](LICENSE) for more details.
