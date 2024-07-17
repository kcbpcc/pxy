from telegram import Bot

# Replace with your actual bot token and user ID
bot_token = '7141714085:AAHlyEzszCy9N-L6wO1zSAkRwGdl0VTQCFI'
chat_id = '-4282665161'

def send_test_message():
    bot = Bot(token=bot_token)
    message = "This is a test message from your bot."
    bot.send_message(chat_id=chat_id, text=message)

if __name__ == "__main__":
    send_test_message()
