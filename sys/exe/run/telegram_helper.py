import telegram

async def send_telegram_message(bot_token, user_usernames, message_text):
    """Send message to Telegram."""
    try:
        bot = telegram.Bot(token=bot_token)
        await bot.send_message(chat_id=user_usernames, text=message_text)
    except Exception as e:
        print(f"Error sending message to Telegram: {e}")
