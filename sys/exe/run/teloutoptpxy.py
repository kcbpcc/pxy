import telegram
async def send_telegram_message(message_text):
    try:
        # Define the bot token and your Telegram username or ID
        bot_token = '6867988078:AAGNBJqs4Rf8MR4xPGoL1-PqDOYouPan7b0'  # Replace with your actual bot token
        user_usernames = '-4136531362'  # Replace with your Telegram username or ID

        # Create a Telegram bot
        bot = telegram.Bot(token=bot_token)

        # Send the message to Telegram
        await bot.send_message(chat_id=user_usernames, text=message_text)

    except Exception as e:
        # Handle the exception (e.g., log it) and continue with your code
        print(f"Error sending message to Telegram: {e}")
