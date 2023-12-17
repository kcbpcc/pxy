from telegram import Bot

# Define the bot token and user ID
bot_token = '6603707685:AAFhWgPpliYjDqeBY24UyDipBbuBavcb4Bo'  # Replace with your actual bot token
user_id = '-4022487175'  # Replace with your Telegram user ID

# Create a bot instance
bot = Bot(token=bot_token)

# Send a test message
test_message = "This is a test message!"
bot.send_message(chat_id=user_id, text=test_message)
