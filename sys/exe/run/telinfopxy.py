import subprocess
import asyncio
import telegram
import io
from PIL import ImageGrab  # This is for Windows, for Linux or Mac you might need different libraries

# Define the bot token and your Telegram username or ID
bot_token = '6409002088:AAH9mu0lfjvHl_IgRAgX7YrjJQa2Ew9qaLo'  # Replace with your actual bot token
user_usernames = '-4022487175'  # Replace with your Telegram username or ID

# Function to send an image to Telegram
async def send_telegram_image(image_bytes):
    bot = telegram.Bot(token=bot_token)
    await bot.send_photo(chat_id=user_usernames, photo=image_bytes)

async def run_and_send_message():
    try:
        # Run the Python program and capture the output
        output = subprocess.check_output(['python3', 'cntrlpxy.py'], text=True)

        # Save the console output as an image
        img = ImageGrab.grab(bbox=(0, 0, 1920, 1080))  # Adjust the coordinates based on your screen resolution
        img_byte_array = io.BytesIO()
        img.save(img_byte_array, format='PNG')
        img_byte_array.seek(0)

        # Send the image via Telegram
        await send_telegram_image(img_byte_array)

    except subprocess.CalledProcessError as e:
        # Handle errors if the subprocess fails
        error_message = f"Error running the program: {e}"
        await send_telegram_message(error_message)

# Run the asynchronous function using asyncio.run
if __name__ == "__main__":
    asyncio.run(run_and_send_message())





