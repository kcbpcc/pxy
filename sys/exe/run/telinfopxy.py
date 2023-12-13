import subprocess
import asyncio
import telegram
from html import escape  # Import escape function to sanitize HTML

# Define the bot token and your Telegram username or ID
bot_token = '6409002088:AAH9mu0lfjvHl_IgRAgX7YrjJQa2Ew9qaLo'  # Replace with your actual bot token
user_usernames = '-4022487175'  # Replace with your Telegram username or ID

# Function to send a message to Telegram
async def send_telegram_message(message_text):
    bot = telegram.Bot(token=bot_token)
    sanitized_message = escape(message_text)  # Sanitize HTML
    await bot.send_message(chat_id=user_usernames, text=sanitized_message, parse_mode='HTML')

async def run_and_send_message():
    try:
        # Run the Python program and capture the output
        output = subprocess.check_output(['python3', 'cntrlpxy.py'], text=True)

        # Send the output as a message via Telegram
        telegram_message = f"Program Output:\n\n{output}"
        await send_telegram_message(telegram_message)

    except subprocess.CalledProcessError as e:
        # Handle errors if the subprocess fails
        error_message = f"Error running the program: {e}"
        await send_telegram_message(error_message)

# Run the asynchronous function using asyncio.run
if __name__ == "__main__":
    asyncio.run(run_and_send_message())




