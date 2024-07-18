import os
import requests
from datetime import datetime

# Function to update log file with today's date
def update_log_file(file_path):
    today_date = datetime.now().strftime('%Y-%m-%d')
    if not os.path.exists(file_path):
        with open(file_path, 'w', newline='') as file:
            file.write(today_date)
    else:
        with open(file_path, 'r') as file:
            last_date = file.read().strip()
        if last_date != today_date:
            with open(file_path, 'w') as file:
                file.write(today_date)

# Function to send summary to Telegram with custom message
def send_summary_to_telegram(message):
    current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    TELEGRAM_BOT_TOKEN = "7163187536:AAG4UaLEj-iUlHENQmnNVE6080E1fZ_Wxtc"
    TELEGRAM_CHAT_ID = "-4143295985"
    summary = (
        f"Date and Time: {current_datetime}\n"
        f"{message}\n"  # Append the custom message here
    )
    message = summary
    
    telegram_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    params = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    
    response = requests.get(telegram_url, params=params)
    
    if response.status_code == 200:
        print("Message sent successfully!")
        # Update the log file with today's date
        log_file = "pxysummary.csv"
        update_log_file(log_file)
    else:
        print(f"Failed to send message: {response.status_code} - {response.text}")

# Function to check if summary has already been sent today
def check_and_send_summary(message):
    log_file = "pxysummary.csv"
    if os.path.exists(log_file):
        with open(log_file, 'r') as file:
            last_date = file.read().strip()
        today_date = datetime.now().strftime('%Y-%m-%d')
        if last_date == today_date:
            print("Summary already sent today. Skipping...")
        else:
            send_summary_to_telegram(message)
    else:
        send_summary_to_telegram(message)

# Example usage:
custom_message = "Custom message content here."
check_and_send_summary(custom_message)
