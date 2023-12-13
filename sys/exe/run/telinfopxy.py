import subprocess
import asyncio
import telegram
from pyth.plugins.plaintext.writer import RtfWriter


# Define the bot token and your Telegram username or ID
bot_token = '6409002088:AAH9mu0lfjvHl_IgRAgX7YrjJQa2Ew9qaLo'  # Replace with your actual bot token
user_usernames = '-4022487175'  # Replace with your Telegram username or ID

# Function to send an RTF message to Telegram
async def send_telegram_rtf_file(rtf_content):
    bot = telegram.Bot(token=bot_token)
    await bot.send_document(chat_id=user_usernames, document=rtf_content, caption='PXY Output.rtf')

async def run_and_send_message():
    try:
        # Run the Python program and capture the output
        output = subprocess.check_output(['python3', '/home/userland/pxy/sys/exe/run/telinfopxy.py'], text=True)

        # Convert the output to RTF format
        rtf_output = RtfWriter.write_plain_text(output)

        # Save the RTF content to a file
        rtf_file_path = '/home/userland/pxy/sys/exe/run/output.rtf'
        with open(rtf_file_path, 'w', encoding='utf-8') as file:
            file.write(rtf_output)

        # Send the RTF content as a document via Telegram
        await send_telegram_rtf_file(open(rtf_file_path, 'rb'))

    except subprocess.CalledProcessError as e:
        # Handle errors if the subprocess fails
        error_message = f"Error running the program: {e}"
        await send_telegram_message(error_message)

# Run the asynchronous function using asyncio.run
if __name__ == "__main__":
    asyncio.run(run_and_send_message())






