from datetime import datetime, timedelta
import pandas as pd
import traceback
import sys
import logging
from login_get_kite import get_kite, remove_token
from cnstpxy import dir_path
from fundpxy import calculate_decision
from nftpxy import OPTIONS
import telegram
import asyncio
from mktpxy import get_market_check

onemincandlesequance, mktpxy = get_market_check()
from nftpxy import nse_action, nse_power, Day_Change, Open_Change, OPTIONS
from optpxy import get_optpxy

optpxy = get_optpxy()
from cyclepxy import cycle
from utcpxy import peak_time

peak = peak_time()
from macdpxy import calculate_macd_signal

macd = calculate_macd_signal("^NSEI")
from smaftypxy import check_nifty_status

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


# Define function to get next Thursday date
def get_next_thursday():
    current_date = datetime.now()
    days_until_next_thursday = (3 - current_date.weekday() + 7) % 7

    # Ensure at least 6 days ahead
    if days_until_next_thursday < 6:
        days_until_next_thursday += 7

    return current_date + timedelta(days=days_until_next_thursday)


# Define function to calculate expiry date for the symbol
def get_symbol_expiry_date(expiry_date):
    expiry_year = expiry_date.strftime("%y")
    expiry_month = expiry_date.strftime("%m")
    expiry_day = expiry_date.strftime("%d")

    # Ensure the month is one digit until October
    if int(expiry_month) < 10:
        expiry_month = expiry_month[1]

    # Ensure the date is always two digits
    expiry_day = expiry_day.zfill(2)

    return expiry_year, expiry_month, expiry_day


# Define function to construct symbol for the NIFTY Put Option
def construct_symbol(expiry_year, expiry_month, expiry_day, option_type):
    return f"NIFTY{expiry_year}{expiry_month}{expiry_day}{OPTIONS}{option_type}"


# Define function to check existing positions for the symbol
def check_existing_positions(broker, symbol):
    try:
        df = pd.read_csv('fileHPdf.csv')
        existing_symbols = set(df['tradingsymbol'].tolist())
    except FileNotFoundError:
        existing_symbols = set()

    positions_response = broker.kite.positions()
    positions_net = positions_response['net']

    for position in positions_net:
        if position['tradingsymbol'] == symbol and position['quantity'] >= 50:
            return True  # Existing positions found

    return symbol in existing_symbols


# Define function to calculate funds needed for the symbol with a given quantity
def calculate_required_funds(broker, symbol, quantity):
    resp = broker.kite.ltp([f"NFO:{symbol}"])
    if resp and isinstance(resp, dict) and f"NFO:{symbol}" in resp:
        ltp = resp[f"NFO:{symbol}"]['last_price']
        return ltp * quantity
    else:
        return None


# Define function to place order for the symbol
async def place_order(broker, symbol):
    try:
        order_id = broker.order_place(
            tradingsymbol=symbol,
            quantity=50,
            exchange="NFO",
            transaction_type='BUY',
            order_type='MARKET',
            product='NRML'
        )

        print(f"DEBUG: {symbol} Ordered")
        message_text = f"Option Order placed successfully. Order ID: {order_id}"
        # Send the message to Telegram
        await send_telegram_message(message_text)
        return True  # Order successful
    except Exception as e:
        print(f"DEBUG: Error placing Option order for {symbol}: {e}")
        return False  # Order failed


# Main function to orchestrate the workflow
async def main():
    try:
        original_stdout = sys.stdout
        # Redirect sys.stdout to 'output.txt'
        with open('output.txt', 'w') as file:
            sys.stdout = file

            try:
                broker = get_kite(api="bypass", sec_dir=dir_path)
                print("DEBUG: Broker initialized successfully.")
            except Exception as e:
                remove_token(dir_path)
                traceback.format_exc()
                logging.error(f"{str(e)} unable to get holdings")
                sys.exit(1)
                print("DEBUG: Broker initialization failed.")
    except Exception as e:
        print(f"DEBUG: Error: {e}")
        sys.exit(1)

    finally:
        # Reset sys.stdout to its original value
        sys.stdout = original_stdout

        next_thursday = get_next_thursday()
        expiry_year, expiry_month, expiry_day = get_symbol_expiry_date(next_thursday)

        # Determine option type based on mktpxy
        if mktpxy in ['Buy', 'Bull']:
            option_type = 'CE'  # Call Option
            print(f"DEBUG: Option type determined: Call Option (CE) for {symbol}")
        elif mktpxy in ['Sell', 'Bear']:
            option_type = 'PE'  # Put Option
            print(f"DEBUG: Option type determined: Put Option (PE) for {symbol}")

        symbol = construct_symbol(expiry_year, expiry_month, expiry_day, option_type)


        if not check_existing_positions(broker, symbol):
            funds_needed = calculate_required_funds(broker, symbol, 50)
            available_cash = broker.kite.margins()["equity"]["available"]["live_balance"]
        
            if funds_needed is not None and available_cash >= 1.1 * funds_needed:
                print("Got funds. Proceeding with order")
                order_placed = await place_order(broker, symbol)
                if not order_placed:
                    print("Order failed. Check error messages.")
            else:
                print("No funds. Order aborted.")
        else:
            print(f"Skip {symbol}.")


