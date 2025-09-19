# Closure's Message Box
A Telegram bot that perodically updates you with ~~Tweets~~ Xs, from your favorite ~~Twitter~~ X account in the last 24 hours.

## Prerequisites
1. [Python](https://www.python.org/downloads/) (Preferably the newest version)
2. [python-telegram-bot](https://pypi.org/project/python-telegram-bot/) (Preferably the newest version)
   ```bat
   pip install python-telegram-bot
   ```
3. [tweepy](https://pypi.org/project/tweepy/) (Preferably the newest version)
   ```bat
   pip install tweepy
   ```

## Running
1. Clone this repository:
   ```bat
   git clone https://github.com/uwungu01-rep/closures-message-box
   ```
   Alternatively, download the [zip](https://github.com/uwungu01-rep/closures-message-box/archive/refs/heads/main.zip) file and unzip it at your desired location.
2. Create a file name data.json in the main folder. The file should look something like this:
   ```json
   {
      "XToken": "YOUR_TWITTER_API_TOKEN",
      "BotToken": "YOUR_TELEGRAM_BOT_TOKEN",
      "AccountHandle": "THE_HANDLE(USERNAME)_OF_THE_ACCOUNT_YOU_WANT_TO_TRACK",
      "ChatID": "THE_ID_OF_THE_CHAT_YOU_WANT_THE_BOT_TO_SEND_UPDATES"
   }
   ```
3. Run ```run.bat```
4. And you're done.

## License
This program is licensed under the GNU General Public License 3.0, see [LICENSE](LICENSE) for more details.
