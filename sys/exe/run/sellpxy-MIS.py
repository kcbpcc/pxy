#PXY®
import sys
import os
import time
import datetime
import subprocess
import warnings
import csv
import random
import asyncio
import logging
import numpy as np
import pandas as pd
import yfinance as yf
from rich import print
from rich.console import Console
from rich.style import Style
import telegram
from colorama import Fore, Style
from cnstpxy import dir_path, sellbuff, secs, perc_col_name
from toolkit.logger import Logger
from toolkit.currency import round_to_paise
from login_get_kite import get_kite, remove_token
from mktpxy import get_market_check
from nftpxy import nse_action, nse_power, Day_Change, Open_Change
from bukdpxy import sum_last_numerical_value_in_each_row
from swchpxy import analyze_stock
from selfpxy import get_random_spiritual_message

############################################"PXY® PreciseXceleratedYield Pvt Ltd™############################################
def order_place(index, row):
    try:
        exchsym = str(index).split(":")
        if len(exchsym) >= 2:
            logging.info(f"Placing order for {exchsym[1]}, {str(row)}")
            order_id = broker.order_place(
                tradingsymbol=exchsym[1],
                exchange=exchsym[0],
                transaction_type='SELL',
                quantity=int(row['qty']),
                order_type='LIMIT',
                product='CNC',
                variety='regular',
                price=round_to_paise(row['ltp'], -0.3)
            )
            if order_id:
                logging.info(f"Order {order_id} placed for {exchsym[1]} successfully")                                
                # Write the row to the CSV file here
                with open(csv_file_path, 'a', newline='') as csvfile:
                    csvwriter = csv.writer(csvfile)
                    csvwriter.writerow(row.tolist())  # Write the selected row to the CSV file
                    try:
                        import telegram
                        import asyncio
                        columns_to_drop = ['smb_power', 'oPL%', 'pstp', '_pstp', 'qty', 'close', 'open', 'high', 'low', 'PL%_H', 'dPL%', 'pxy','yxp']
                        # Dropping specified columns from the row
                        for column in columns_to_drop:
                            if column in row:
                                del row[column]
                        message_text = f"{str(row):>10} \nhttps://www.tradingview.com/chart/?symbol={key}\nBooked profit until now: {result}"
                        # Define the bot token and your Telegram username or ID
                        bot_token = '6409002088:AAH9mu0lfjvHl_IgRAgX7YrjJQa2Ew9qaLo'  # Replace with your actual bot token
                        user_usernames = ('-4022487175')  # Replace with your Telegram username or ID
                        # Function to send a message to Telegram
                        async def send_telegram_message(message_text):
                            bot = telegram.Bot(token=bot_token)
                            await bot.send_message(chat_id=user_usernames, text=message_text)
                    except Exception as e:
                        # Handle the exception (e.g., log it) and continue with your code
                        print(f"Error sending message to Telegram: {e}")
                    # Send the 'row' content as a message to Telegram immediately after printing the row
                    loop = asyncio.get_event_loop()
                    loop.run_until_complete(send_telegram_message(message_text))
                return True                
            else:
                logging.error("Order placement failed")       
        else:
            logging.error("Invalid format for 'index'")    
    except Exception as e:
        #print(traceback.format_exc())
        logging.error(f"{str(e)} while placing order")
    return False
############################################"PXY® PreciseXceleratedYield Pvt Ltd™############################################

# Set the python3IOENCODING environment variable to 'utf-8'
sys.stdout.reconfigure(encoding='utf-8')

# Suppress yfinance warnings
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)

# Specify the stock symbol (NIFTY 50)
symbol = '^NSEI'

# Intervals
intervals = [5, 4, 3, 2, 1]
periods = [1, 2, 3, 4, 5]

# Create a Console instance for rich print formatting
console = Console()

# Function to calculate the Heikin-Ashi candle colors for the last three closed candles
def calculate_last_three_heikin_ashi_colors(symbol, interval):
    # Check if the current time is within the specified time range (3:45 AM to 4:00 AM UTC)
    current_utc_time = time.gmtime().tm_hour * 60 + time.gmtime().tm_min

    if 222 <= current_utc_time < 233:
        sys.stdout = open(os.devnull, 'w')

        # Download data for the specified number of days (fixed to 5 days)
        data = yf.download(symbol, period="5d")
        
        # Extract today's open, yesterday's close, and current price
        today_open = data['Open'].iloc[-1]
        today_high = data['High'].iloc[-1]
        today_low = data['Low'].iloc[-1]
        current_price = data['Close'].iloc[-1]
        
        yesterday_close = data['Close'].iloc[-2]
        yesterday_open = data['Open'].iloc[-2]
        
        sys.stdout.close()
        sys.stdout = sys.__stdout__

        day_open = today_open  # Open of the day
        ltp = current_price  # Last traded price
    
        current_color = 'Bear' if day_open > ltp else 'Bull'
        last_closed_color = 'Bear' if day_open > ltp else 'Bull'
        second_closed_color = 'Bear' if day_open > ltp else 'Bull'
    else:
        # Fetch real-time data for the specified interval
        data = yf.Ticker(symbol).history(period=f'{periods[0]}d', interval=f'{interval}m')

        # Calculate Heikin-Ashi candles
        ha_close = (data['Open'] + data['High'] + data['Low'] + data['Close']) / 4
        ha_open = (data['Open'].shift(1) + data['Close'].shift(1)) / 2

        # Calculate the colors of the last three closed candles
        current_color = 'Bear' if ha_close.iloc[-1] < ha_open.iloc[-1] else 'Bull'
        last_closed_color = 'Bear' if ha_close.iloc[-2] < ha_open.iloc[-2] else 'Bull'
        second_closed_color = 'Bear' if ha_close.iloc[-3] < ha_open.iloc[-3] else 'Bull'

    return current_color, last_closed_color, second_closed_color

def get_smbpxy_check(symbol):
    try:
        # Loop through all intervals and periods
        for interval in intervals:
            for period in periods:
                current_color, last_closed_color, second_closed_color = calculate_last_three_heikin_ashi_colors(symbol, interval)

                if current_color and last_closed_color:
                    if current_color == 'Bear' and last_closed_color == 'Bear' and second_closed_color == 'Bear':
                        return 'Bear'
                    elif current_color == 'Bull' and last_closed_color == 'Bull' and second_closed_color == 'Bull':
                        return 'Bull'
                    elif current_color == 'Bear' and last_closed_color == 'Bear' and second_closed_color == 'Bull':
                        return 'Sell'
                    elif current_color == 'Bull' and last_closed_color == 'Bull' and second_closed_color == 'Bear':
                        return 'Buy'
                    else:
                        return 'NONE'

        return 'NONE'

    except Exception as e:
        console.print(f"[red]Error determining smbpxy check: {e}[/red]")
        return 'NONE'

############################################"PXY® PreciseXceleratedYield Pvt Ltd™############################################

csv_file_path = 'zlistpxy.csv'
symbol_df = pd.read_csv(csv_file_path, header=0)  # Assuming the header is in the first row

# Process each symbol
for symbol_row in symbol_df['STOCK']:
    symbol = f"{symbol_row}.NS"  # Append ".NS" to each symbol
    smbpxy_check = get_smbpxy_check(symbol)
    console = Console()
    console.print(f"[bold]{symbol}:[/bold] ", end="")
    
    if "Buy" in smbpxy_check:
        console.print(f"[green]{smbpxy_check}[/green] 🟢🟢🟢")
    elif "Sell" in smbpxy_check:
        console.print(f"[green]{smbpxy_check}[/green] 🔴🔴🔴")

