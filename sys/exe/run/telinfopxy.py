import subprocess
import schedule
import time
import telegram

# Define the bot token and your Telegram username or ID
bot_token = '6409002088:AAH9mu0lfjvHl_IgRAgX7YrjJQa2Ew9qaLo'  # Replace with your actual bot token
user_usernames = ('-4022487175')  # Replace with your Telegram username or ID


# Function to send a message to Telegram
async def send_telegram_message(message_text):
    bot = telegram.Bot(token=bot_token)
    await bot.send_message(chat_id=user_usernames, text=message_text)

def run_and_send_message():
    try:
        # Run the Python program and capture the output
        output = subprocess.check_output(['python3', cntrlpxy.py], text=True)

        # Send the output as a message via Telegram
        telegram_message = f"Program Output:\n\n{output}"
        send_telegram_message(telegram_message)

    except subprocess.CalledProcessError as e:
        # Handle errors if the subprocess fails
        error_message = f"Error running the program: {e}"
        send_telegram_message(error_message)

# Schedule the task to run every hour from 3:30 AM to 9:30 AM UTC
schedule.every().hour.at(':30').do(run_and_send_message).tag('task')

# Run the scheduler
while True:
    schedule.run_pending()
    time.sleep(1)
