import subprocess
import asyncio
import telegram
from html import escape


# Define the bot token and your Telegram username or ID
bot_token = '6409002088:AAH9mu0lfjvHl_IgRAgX7YrjJQa2Ew9qaLo'  # Replace with your actual bot token
user_usernames = '-4022487175'  # Replace with your Telegram username or ID

# Function to send an HTML message to Telegram
async def send_telegram_html_file(html_content):
    bot = telegram.Bot(token=bot_token)
    sanitized_html = escape(html_content)  # Sanitize HTML
    await bot.send_message(chat_id=user_usernames, text=sanitized_html, parse_mode='HTML')

async def run_and_send_message():
    try:
        # Run the Python program and capture the HTML output
        output = subprocess.check_output(['python3', 'cntrlpxy.py'], text=True)

        # Create an HTML file with the program output
        html_content = f"<pre>{escape(output)}</pre>"

        # Save the HTML content to a file
        html_file_path = 'output.html'
        with open(html_file_path, 'w', encoding='utf-8') as file:
            file.write(html_content)

        # Send the HTML content as a message via Telegram
        await send_telegram_html_file(html_content)

    except subprocess.CalledProcessError as e:
        # Handle errors if the subprocess fails
        error_message = f"Error running the program: {e}"
        await send_telegram_message(error_message)

# Run the asynchronous function using asyncio.run
if __name__ == "__main__":
    asyncio.run(run_and_send_message())





