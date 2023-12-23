import requests
from telegram import Bot
from telegram import InputFile

# Replace 'YOUR_BOT_TOKEN' with your actual Telegram bot token
BOT_TOKEN = "6396096532:AAG5adz_SeUwV8WLn7miteljk_pRrpt8mO0"

# Replace 'YOUR_CHAT_ID' with your chat ID
CHAT_ID = "-4067167377"

# Replace '/home/userland/pxy/sys/exe/run/bordpxy.txt' with the actual path to your file
FILE_PATH = "/home/userland/pxy/sys/exe/run/bordpxy.txt"

def send_file_to_telegram(file_path, chat_id, bot_token):
    bot = Bot(token=bot_token)
    with open(file_path, "rb") as file:
        bot.send_document(chat_id=chat_id, document=file)

# Send the file to Telegram
send_file_to_telegram(FILE_PATH, CHAT_ID, BOT_TOKEN)
