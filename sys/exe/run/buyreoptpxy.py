from datetime import datetime, timedelta
import pandas as pd
import traceback
import sys
import asyncio
import telegram
from toolkit.logger import Logger
from toolkit.currency import round_to_paise
from toolkit.utilities import Utilities
from login_get_kite import get_kite, remove_token
from cnstpxy import dir_path, fileutils, buybuff, max_target
from buypluspxy import Trendlyne
from fundpxy import calculate_decision
from nftpxy import OPTIONS

# Define the get_ltp function
def get_ltp(exchange, symbol, broker):
    key = f"{exchange}:{symbol}"
    resp = broker.kite.ltp([key])
    
    if resp and isinstance(resp, dict) and key in resp:
        return resp[key]['last_price']
    else:
        return None  # Return None if the ltp is not available or if there is an issue

# Define the calculate_funds_needed function
def calculate_funds_needed(exchange, symbol, broker):
    ltp = get_ltp(exchange, symbol, broker)
    if ltp is not None:
        return ltp * 50
    else:
        return None

# Store the original stdout
original_stdout = sys.stdout

# Define a function to encapsulate the main logic
def execute_program(symbol):
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

    # Read the CSV file to check if symbols exist
    try:
        df = pd.read_csv('fileHPdf.csv')
        existing_symbols = set(df['tradingsymbol'].tolist())
    except FileNotFoundError:
        existing_symbols = set()

    # Check if the symbol exists in the CSV file (as is)
    if symbol in existing_symbols:
        # Check if the quantity is greater than 0
        if df.loc[df['tradingsymbol'] == symbol, 'quantity'].iloc[0] > 0:
            print(f"{symbol} exists with quantity greater than 0 in the CSV file.")
            sys.exit(0)  # Exit the program

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

    # Construct the symbol for the NIFTY Put Option
    symbol_OPTIONS = f"NIFTY{expiry_year}{expiry_month}{expiry_day}{OPTIONS}CE"

    # Check against available cash with a buffer of 10%
    response = broker.kite.margins()
    available_cash = response["equity"]["available"]["live_balance"]

    # Calculate funds needed for the options symbol with quantity 50
    funds_needed_OPTIONS = calculate_funds_needed("NFO", symbol_OPTIONS, broker)

    # Print results
    if funds_needed_OPTIONS is not None:
        if available_cash >= 1.1 * funds_needed_OPTIONS:
            print("You have sufficient funds. Proceeding with order placement.")

            # Place order here
            try:
                order_id_OPTIONS = broker.order_place(
                    tradingsymbol=symbol_OPTIONS,
                    quantity=50,
                    exchange="NFO",
                    transaction_type='BUY',
                    order_type='MARKET',
                    product='NRML'
                )

                print("Put Option Order placed successfully. Order ID:", order_id_OPTIONS)
                message_text_OPTIONS = f"Put Option Order placed successfully. Order ID: {order_id_OPTIONS}"
                # Send the message to Telegram
                asyncio.run(send_telegram_message(message_text_OPTIONS))

            except Exception as e:
                print("Error placing Put Option order:", e)

        else:
            print("Insufficient funds. Order placement aborted.")
    else:
        print("Unable to calculate funds needed for the symbol.")





