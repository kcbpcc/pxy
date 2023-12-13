import subprocess
import asyncio
import telegram
from html import escape


# Define the bot token and your Telegram username or ID
bot_token = '6409002088:AAH9mu0lfjvHl_IgRAgX7YrjJQa2Ew9qaLo'  # Replace with your actual bot token
user_usernames = '-4022487175'  # Replace with your Telegram username or ID

# Function to read HTML content from a file
def read_html_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

# Function to send an HTML message to Telegram
async def send_telegram_html_file(html_content):
    bot = telegram.Bot(token=bot_token)
    sanitized_html = escape(html_content)  # Sanitize HTML
    await bot.send_message(chat_id=user_usernames, text=sanitized_html, parse_mode='HTML')

async def run_and_send_message():
    try:
        # Run the Python program and capture the HTML output in a file
        subprocess.run(['python3', 'cntrlpxy.py'], check=True)

        # Read the HTML content from the file in the same directory
        html_file_path = 'output.html'  # Assuming the HTML file is in the same directory
        html_content = read_html_file(html_file_path)

        # Send the HTML content as a message via Telegram
        await send_telegram_html_file(html_content)

    except subprocess.CalledProcessError as e:
        # Handle errors if the subprocess fails
        error_message = f"Error running the program: {e}"
        await send_telegram_message(error_message)

# Run the asynchronous function using asyncio.run
if __name__ == "__main__":
    asyncio.run(run_and_send_message())





