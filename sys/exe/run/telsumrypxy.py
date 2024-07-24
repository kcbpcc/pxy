import os
import requests
from datetime import datetime

# Function to update log file with current date and hour and source
def update_log_file(file_path, source):
    current_datetime = datetime.now().strftime('%Y-%m-%d %H')  # Only include the hour
    new_entry = f"{source},{current_datetime}"
    
    if not os.path.exists(file_path):
        with open(file_path, 'w', newline='') as file:
            file.write("source,datetime\n")  # Write header
            file.write(f"{new_entry}\n")  # Initial entry
    else:
        # Read existing entries and check for duplicates
        entries = set()
        with open(file_path, 'r') as file:
            lines = file.readlines()
            for line in lines[1:]:  # Skip header line
                parts = line.strip().split(',')
                if len(parts) >= 2:
                    entry = (parts[0], parts[1])  # (source, datetime)
                    entries.add(entry)
        
        # Remove entries older than the current hour
        current_hour = datetime.now().strftime('%Y-%m-%d %H')
        entries = {entry for entry in entries if entry[1] == current_hour}
        
        # Append new entry if not already present
        if (source, current_datetime) not in entries:
            with open(file_path, 'a') as file:
                file.write(f"{new_entry}\n")

# Function to send summary to Telegram with custom message
def send_summary_to_telegram(message, source):
    current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    TELEGRAM_BOT_TOKEN = "7163187536:AAG4UaLEj-iUlHENQmnNVE6080E1fZ_Wxtc"
    TELEGRAM_CHAT_ID = "-4143295985"
    summary = (
        f"{message}\n"  # Append the custom message here
    )
    message = summary
    
    telegram_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    params = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True
    }

    
    response = requests.get(telegram_url, params=params)
    
    if response.status_code == 200:
        #print("📢📢  Update just sent successfully   📢📢")
        # Update the log file with current date and hour and source
        log_file = "pxysummary.csv"
        update_log_file(log_file, source)
    else:
        print(f"Failed to send message: {response.status_code} - {response.text}")

# Function to check if summary has already been sent this hour
def check_and_send_summary(message, source):
    log_file = "pxysummary.csv"
    current_hour = datetime.now().strftime('%Y-%m-%d %H')
    already_sent = False
    
    if os.path.exists(log_file):
        with open(log_file, 'r') as file:
            lines = file.readlines()
            for line in lines[1:]:  # Skip header line
                parts = line.strip().split(',')
                if len(parts) >= 2:
                    log_source, log_hour = parts
                    if log_source == source and log_hour == current_hour:
                        already_sent = True
                        break
        
    if already_sent:
        pass  # Do nothing
        #print("🔔🔔Update already sent for this hour 🔔🔔")
    else:
        send_summary_to_telegram(message, source)
