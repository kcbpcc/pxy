import asyncio
from telegram import Bot

async def send_test_message():
    # Define the bot token and user ID
    bot_token = '6409002088:AAH9mu0lfjvHl_IgRAgX7YrjJQa2Ew9qaLo'  # Replace with your actual bot token
    user_id = '-4022487175'  # Replace with your Telegram user ID

    # Create a bot instance
    bot = Bot(token=bot_token)

    # Send a test message
    test_message = "This is a test message!"
    await bot.send_message(chat_id=user_id, text=test_message)

# Run the event loop
asyncio.run(send_test_message())

