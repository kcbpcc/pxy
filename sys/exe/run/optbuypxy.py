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
from buypluspxy import Trendlyne
from fundpxy import calculate_decision
from nftpxy import OPTIONS
import pandas as pd
decision = calculate_decision()
import telegram
import asyncio
# Store the original stdout
original_stdout = sys.stdout

try:
    # Redirect sys.stdout to 'output.txt'
    with open('output.txt', 'w') as file:
        sys.stdout = file

        try:
            broker = get_kite(api="bypass", sec_dir=dir_path)
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
        bot_token = '6924826872:AAHTiMaXmjyYbGsCFhdZlRRXkyfZTpsKPug'  # Replace with your actual bot token
        user_usernames = ('-4136531362')  # Replace with your Telegram username or ID

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

def get_ltp(exchange, symbol):
    key = f"{exchange}:{symbol}"
    resp = broker.kite.ltp([key])
    
    if resp and isinstance(resp, dict) and key in resp:
        return resp[key]['last_price']
    else:
        return None  # Return None if the ltp is not available or if there is an issue

# Function to calculate funds needed for a given symbol and quantity
def calculate_funds_needed(exchange, symbol, quantity):
    ltp = get_ltp(exchange, symbol)
    if ltp is not None:
        return ltp * quantity
    else:
        return None

# Construct the symbol for the NIFTY Put Option
symbol_PE = f"NIFTY{expiry_year}{expiry_month}{expiry_day}{OPTIONS}PE"
symbol_CE = f"NIFTY{expiry_year}{expiry_month}{expiry_day}{OPTIONS}CE"

# Calculate funds needed for each symbol with quantity 50
quantity = 50
funds_needed_PE = calculate_funds_needed("NFO", symbol_PE, quantity)
funds_needed_CE = calculate_funds_needed("NFO", symbol_CE, quantity)

# Check against available cash with a buffer of 10%
response = broker.kite.margins()
available_cash = response["equity"]["available"]["live_balance"]

# Print results
if funds_needed_PE is not None and funds_needed_CE is not None:
    total_funds_needed = funds_needed_PE + funds_needed_CE
    #print(f"Funds needed for {symbol_PE} with quantity {quantity}: {funds_needed_PE}")
    #print(f"Funds needed for {symbol_CE} with quantity {quantity}: {funds_needed_CE}")
    #print(f"Total funds needed: {total_funds_needed}")

    # Read the CSV file to check if symbols exist
    try:
        df = pd.read_csv('fileHPdf.csv')
        existing_symbols = set(df['tradingsymbol'].tolist())
    except FileNotFoundError:
        existing_symbols = set()

    # Check if either of the symbols exists in the CSV file
    if symbol_PE in existing_symbols or symbol_CE in existing_symbols:
        print(f"I got {symbol_PE} or {symbol_CE}")
        sys.exit(0)  # Exit the program

    if available_cash >= 1.1 * total_funds_needed:
        print("You have sufficient funds. Proceeding with order placement.")
        
        # Place orders here
        try:
            order_id_PE = broker.order_place(
                tradingsymbol=symbol_PE,
                quantity=50,
                exchange="NFO",
                transaction_type='BUY',
                order_type='MARKET',
                product='NRML'
            )

            print("Put Option Order placed successfully. Order ID:", order_id_PE)
            message_text_PE = f"Put Option Order placed successfully. Order ID: {order_id_PE}"
            # Send the message to Telegram
            asyncio.run(send_telegram_message(message_text_PE))

        except Exception as e:
            print("Error placing Put Option order:", e)
            order_id_PE = None  # Set order_id_PE to None to indicate failure

        try:
            order_id_CE = broker.order_place(
                tradingsymbol=symbol_CE,
                quantity=50,
                exchange="NFO",
                transaction_type='BUY',
                order_type='MARKET',
                product='NRML'
            )

            print("Call Option Order placed successfully. Order ID:", order_id_CE)
            message_text_CE = f"Call Option Order placed successfully. Order ID: {order_id_CE}"
            # Send the message to Telegram
            asyncio.run(send_telegram_message(message_text_CE))

        except Exception as e:
            print("Error placing Call Option order:", e)
            order_id_CE = None  # Set order_id_CE to None to indicate failure

        # Check if both orders were successful
        if order_id_PE is not None and order_id_CE is not None:
            print("Both orders placed successfully. Order IDs:", order_id_PE, order_id_CE)
        else:
            print("At least one order failed. Check error messages.")

    else:
        print("Insufficient funds. Order placement aborted.")
else:
    print("Unable to calculate funds needed for one or more symbols.")

