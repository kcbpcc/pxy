import os
import requests
from datetime import datetime

# Function to update log file with today's date and source
def update_log_file(file_path, source):
    today_date = datetime.now().strftime('%Y-%m-%d')
    new_entry = f"{source},{today_date}"
    
    if not os.path.exists(file_path):
        with open(file_path, 'w', newline='') as file:
            file.write("source,date\n")  # Write header
            file.write(f"{new_entry}\n")  # Initial entry
    else:
        # Read existing entries and check for duplicates
        entries = set()
        with open(file_path, 'r') as file:
            lines = file.readlines()
            for line in lines[1:]:  # Skip header line
                parts = line.strip().split(',')
                if len(parts) >= 2:
                    entry = (parts[0], parts[1])  # (source, date)
                    entries.add(entry)
        
        # Append new entry if not already present
        if (source, today_date) not in entries:
            with open(file_path, 'a') as file:
                file.write(f"{new_entry}\n")

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
        # Update the log file with today's date and source
        log_file = "pxysummary.csv"
        update_log_file(log_file, "AutoUpdate")
    else:
        print(f"Failed to send message: {response.status_code} - {response.text}")

# Function to check if summary has already been sent today
def check_and_send_summary(message, source):
    log_file = "pxysummary.csv"
    if os.path.exists(log_file):
        with open(log_file, 'r') as file:
            lines = file.readlines()
            if len(lines) > 1:  # Check if file has more than header
                last_entry = lines[-1].strip().split(',')
                last_date = last_entry[1] if len(last_entry) > 1 else ''
                if last_date == datetime.now().strftime('%Y-%m-%d'):
                    print("Summary already sent today. Skipping...")
                    return
        
        # Send summary if not already sent today
        send_summary_to_telegram(message)
    else:
        send_summary_to_telegram(message)

# Example usage:
# message = "Your summary message here."
# source = "AutoUpdate"  # Replace with your source identifier
# check_and_send_summary(message, source)

