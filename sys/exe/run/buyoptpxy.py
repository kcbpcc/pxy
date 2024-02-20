from datetime import datetime, timedelta
import pandas as pd
import traceback
import sys
import time
import select
from toolkit.logger import Logger
from toolkit.currency import round_to_paise
from toolkit.utilities import Utilities
from login_get_kite import get_kite, remove_token
from cnstpxy import dir_path, fileutils, buybuff, max_target
from fundpxy import calculate_decision
from nftpxy import OPTIONS
import pandas as pd
import telegram
import asyncio

# Store the original stdout
original_stdout = sys.stdout

try:
    # Redirect sys.stdout to 'output.txt'
    with open('output.txt', 'w') as file:
        sys.stdout = file

        try:
            broker = get_kite(api="bypass", sec_dir=dir_path)  # Placeholders for parameters
        except Exception as e:
            remove_token(dir_path)
            print(traceback.format_exc())
            logging.error(f"{str(e)} unable to get holdings")
            sys.exit(1)

finally:
    # Reset sys.stdout to its original value
    sys.stdout = original_stdout

# Define the function to send a message to Telegram
async def send_telegram_message(message_text):
    try:
        # Define the bot token and your Telegram username or ID
        bot_token = 'YOUR_BOT_TOKEN_HERE'  # Replace with your actual bot token
        user_usernames = ('YOUR_TELEGRAM_USER_ID_HERE')  # Replace with your Telegram username or ID

        # Create a Telegram bot
        bot = telegram.Bot(token=bot_token)

        # Send the message to Telegram
        await bot.send_message(chat_id=user_usernames, text=message_text)

    except Exception as e:
        # Handle the exception (e.g., log it) and continue with your code
        print(f"Error sending message to Telegram: {e}")

# Ensure that the 'broker' object has an 'order_place' method
if not hasattr(broker, 'order_place') or not callable(getattr(broker, 'order_place', None)):
    print("Error: 'broker' object does not have 'order_place' method.")
    sys.exit(1)

# Function to get the symbol based on option type (CE/PE)
def get_option_symbol(option_type, expiry_year, expiry_month, expiry_day):
    if option_type == "CE":
        return f"NIFTY{expiry_year}{expiry_month}{expiry_day}{OPTIONS}CE"
    elif option_type == "PE":
        return f"NIFTY{expiry_year}{expiry_month}{expiry_day}{OPTIONS}PE"
    else:
        raise ValueError("Invalid option type. Must be 'CE' or 'PE'.")

# Function to calculate funds needed for a given symbol and quantity
def calculate_funds_needed(exchange, symbol, quantity):
    ltp = get_ltp(exchange, symbol)  # Placeholder for exchange and symbol parameters
    if ltp is not None:
        return ltp * quantity
    else:
        return None

# Calculate the next Thursday date at least 6 days ahead
current_date = datetime.now()
days_until_next_thursday = (3 - current_date.weekday() + 7) % 7

# Ensure at least 6 days ahead
if days_until_next_thursday < 6:
    days_until_next_thursday += 7

next_thursday = current_date + timedelta(days=days_until_next_thursday)

# Format the date, month, and year
expiry_year = next_thursday.strftime("%y")
expiry_month = next_thursday.strftime("%m")
expiry_day = next_thursday.strftime("%d")

# Ensure the month is one digit until October
if int(expiry_month) < 10:
    expiry_month = expiry_month[1]

# Ensure the date is always two digits
expiry_day = expiry_day.zfill(2)

# Define the option type (CE or PE) based on mktpxy
mktpxy = "Buy"  # Placeholder for mktpxy value
if mktpxy == "Buy":
    option_type = "CE"
elif mktpxy == "Sell":
    option_type = "PE"
else:
    print("Invalid mktpxy value.")
    sys.exit(1)

# Get the option symbol based on option type
symbol_option = get_option_symbol(option_type, expiry_year, expiry_month, expiry_day)

# Calculate funds needed for the option symbol with quantity 50
quantity = 50
funds_needed_option = calculate_funds_needed("NFO", symbol_option, quantity)  # Placeholder for exchange parameter

# Check against available cash with a buffer of 10%
response = broker.kite.margins()
available_cash = response["equity"]["available"]["live_balance"]

if funds_needed_option is not None:
    # Read the CSV file to check if symbols exist
    try:
        df = pd.read_csv('fileHPdf.csv')
        existing_symbols = set(df['tradingsymbol'].tolist())
    except FileNotFoundError:
        existing_symbols = set()

    # Retrieve positions data
    positions_response = broker.kite.positions()
    
    # Access the 'net' key to get positions information
    positions_net = positions_response['net']
    
    # Create a list to store positions info
    positions_info = []
    
    # Store positions information in the list
    for position in positions_net:
        positions_info.append({
            'tradingsymbol': position['tradingsymbol'],
            'quantity': position['quantity']
        })

    # Check if the symbol exists in the CSV file
    if symbol_option in existing_symbols:
        # Check if the quantity is greater than or equal to 50 in the CSV file
        if df.loc[df['tradingsymbol'] == symbol_option, 'quantity'].iloc[0] >= 50:
            print(f"You already have 50 of {symbol_option}. Cannot buy more. Skipping order placement.")
            sys.exit(0)  # Exit the program
    
        # Check if the quantity is greater than 50 in the positions
        for position in positions_info:
            if position['tradingsymbol'] == symbol_option and position['quantity'] > 50:
                print(f"You already have more than 50 of {symbol_option}. Cannot buy more. Skipping order placement.")
                sys.exit(0)  # Exit the program

    if available_cash >= 1.1 * funds_needed_option:
        print("No Funds")
        
        # Place order here
        try:
            order_id_option = broker.order_place(
                tradingsymbol=symbol_option,
                quantity=50,
                exchange="NFO",
                transaction_type='BUY',
                order_type='MARKET',
                product='NRML'
            )

            print(f"{symbol_option} Ordered")
            message_text_option = f"{option_type} Option Order placed successfully. Order ID: {order_id_option}"
            # Send the message to Telegram
            asyncio.run(send_telegram_message(message_text_option))

        except Exception as e:
            print(f"Error placing {option_type} Option order:", e)
            order_id_option = None  # Set order_id_option to None to indicate failure

        # Check if the order was successful
        if order_id_option is not None:
            print(f"{symbol_option} Ordered")
        else:
            print("Order failed")

    else:
        print("No funds. No Order")
else:
    print("Unable to calculate funds needed for the symbol.")

