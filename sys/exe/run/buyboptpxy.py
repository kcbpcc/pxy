from datetime import datetime, timedelta
import pandas as pd
import traceback
import sys
import logging
import telegram
import asyncio
from login_get_kite import get_kite, remove_token
from cnstpxy import dir_path
from mktpxy import get_market_check
from nftpxy import nse_action, nse_power, Day_Change, Open_Change
from strikpxy import get_prices
_, boptions, _, _ = get_prices()
from optpxy import get_optpxy
from cyclepxy import cycle
from utcpxy import peak_time
from macdpxy import calculate_macd_signal
from smaftypxy import check_nifty_status
from mktrndpxy import get_market_status_for_symbol
bmktpxy = get_market_status_for_symbol('^NSEBANK')

onemincandlesequance, mktpxy = get_market_check()
optpxy = get_optpxy()
peak = peak_time()
macd = calculate_macd_signal("^NSEI")
SMAfty = check_nifty_status()

# Define the function to send a message to Telegram
async def send_telegram_message(message_text):
    try:
        # Define the bot token and your Telegram username or ID
        bot_token = '6924826872:AAHTiMaXmjyYbGsCFhdZlRRXkyfZTpsKPug'  # Replace with your actual bot token
        user_usernames = '-4135910842'  # Replace with your Telegram username or ID

        # Create a Telegram bot
        bot = telegram.Bot(token=bot_token)

        # Send the message to Telegram
        await bot.send_message(chat_id=user_usernames, text=message_text)

    except Exception as e:
        # Handle the exception (e.g., log it) and continue with your code
        print(f"Error sending message to Telegram: {e}")

# Define function to get this week's Wednesday date
def get_this_wednesday():
    current_date = datetime.now()
    days_until_this_wednesday = (2 - current_date.weekday() + 7) % 7

    # Ensure the expiry day is always Wednesday
    expiry_date = current_date + timedelta(days=days_until_this_wednesday)
    expiry_year = expiry_date.strftime("%y")
    expiry_month = expiry_date.strftime("%m")
    expiry_day = expiry_date.strftime("%d")

    # Ensure the month is one digit until October
    if int(expiry_month) < 10:
        expiry_month = expiry_month[1]

    # Ensure the date is always two digits
    expiry_day = expiry_day.zfill(2)

    return expiry_year, expiry_month, expiry_day

# Define function to construct symbol for the Bank Nifty Option
def construct_symbol(expiry_year, expiry_month, expiry_day, option_type):
    return f"BANKNIFTY{expiry_year}{expiry_month}{expiry_day}{boptions}{option_type}"

# Define function to check existing positions for the symbol
def check_existing_positions(broker, symbol):
    positions_response = broker.kite.positions()
    positions_net = positions_response['net']

    for position in positions_net:
        if position['tradingsymbol'] == symbol and position['quantity'] >= 20:
            return True  # Existing positions found

    return False

# Define function to place order for the symbol
async def place_order(broker, symbol):
    try:
        order_id = broker.order_place(
            tradingsymbol=symbol,
            quantity=20,
            exchange="NFO",
            transaction_type='BUY',
            order_type='MARKET',
            product='NRML'
        )

        print(f"{symbol} Ordered")
        message_text = f"Option Order {symbol} placed successfully."
        # Send the message to Telegram
        await send_telegram_message(message_text)
        return True  # Order successful
    except Exception as e:
        print(f"Error placing Option order for {symbol}: {e}")
        return False  # Order failed

# Main function to orchestrate the workflow
async def main():
    symbol = None  # Initialize symbol with a default value

    try:
        # Redirect sys.stdout to 'output.txt'
        with open('output.txt', 'w') as file:
            sys.stdout = file

            try:
                broker = get_kite(api="bypass", sec_dir=dir_path)
            except Exception as e:
                remove_token(dir_path)
                traceback.format_exc()
                logging.error(f"{str(e)} unable to get holdings")
                sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

    finally:
        # Reset sys.stdout to its original value
        sys.stdout = sys.__stdout__

    expiry_year, expiry_month, expiry_day = get_this_wednesday()
    option_type = None  # Default value
    
    # Determine option type based on bmktpxy
    if bmktpxy == 'Bull':
        option_type = 'CE'  # Call Option
    elif bmktpxy == 'Sell':
        option_type = 'PE'  # Put Option
    else:
        # Handle the case where bmktpxy doesn't match any condition
        # You can raise an exception, set a default value, or handle it in another way
        print("Check:", "mkt=", bmktpxy, "|nse=", nse_action, "|sma=", SMAfty)
        sys.exit(0)  # For example, exit the program with an error status
    
    symbol = construct_symbol(expiry_year, expiry_month, expiry_day, option_type)

    if check_existing_positions(broker, symbol):
        print(f"already there {symbol}.")
    else:
        order_placed = await place_order(broker, symbol)
        if not order_placed:
            print("Order failed. Check error messages.")

# Define async function to run main function
async def run_main():
    await main()

# Run the main asynchronous function
asyncio.run(run_main())
