from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

with open("./main/token.txt") as file:
    TOKEN = file.read()

with open("./main/xtoken.txt") as file:
    XTOKEN = file.read()



def main():
    ...

if __name__ == "__main__":
    main()