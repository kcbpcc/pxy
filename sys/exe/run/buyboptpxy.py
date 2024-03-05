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
from bnkpxy import bnk_action, bnk_power, Day_bnk_Change, Open_bnk_Change
from strikpxy import get_prices
_, boptions, _, _ = get_prices()
from cyclepxy import cycle
from utcpxy import peak_time
from macdpxy import calculate_macd_signal
from smapxy import check_index_status
from mktrndpxy import get_market_status_for_symbol
bmktpxy = get_market_status_for_symbol('^NSEBANK')
peak = peak_time()
macd = calculate_macd_signal('^NSEBANK')
SMAfty = check_index_status('^NSEBANK')
from smaoptpxy import sma_above_or_below
smabank = sma_above_or_below('^NSEBANK')
async def send_telegram_message(message_text):
    try:
        bot_token = '6924826872:AAHTiMaXmjyYbGsCFhdZlRRXkyfZTpsKPug'  # Replace with your actual bot token
        user_usernames = '-4135910842'  # Replace with your Telegram username or ID
        bot = telegram.Bot(token=bot_token)
        await bot.send_message(chat_id=user_usernames, text=message_text)
    except Exception as e:
        print(f"Error sending message to Telegram: {e}")
def get_this_month_expiry():
    current_date = datetime.now()
    this_month = current_date.replace(day=1) + timedelta(days=15)
    this_month = this_month.replace(day=1)
    expiry_year = this_month.strftime("%y")
    expiry_month = this_month.strftime("%b").upper()  
    return expiry_year, expiry_month
def construct_symbol(expiry_year, expiry_month, option_type, broker):
    symbol = f"BANKNIFTY{expiry_year}{expiry_month}"
    open_positions_count = 0  # Counter to keep track of open positions with quantity > 0

    # Count open positions with quantity > 0 for the given option type
    for position in broker.kite.positions()['net']:
        if position['tradingsymbol'].startswith('BANKNIFTY') and position['tradingsymbol'].endswith(option_type) and position['quantity'] > 0:
            open_positions_count += 1

    # Check if the number of open positions exceeds the limit
    if SMAfty == "up":
        if option_type == "CE" and open_positions_count >= 3:
            print("Got 3 Call open positions, So dont buy")
            return None
        elif option_type == "PE" and open_positions_count >= 1:
            print("Got 1 Put open positions, So dont buy")
            return None
    elif SMAfty == "down":
        if option_type == "PE" and open_positions_count >= 3:
            print("Got 3 Put open positions, So dont buy")
            return None
        elif option_type == "CE" and open_positions_count >= 1:
            print("Got 1 Call open positions, So dont buy")
            return None

    # Define the symbol range for adjustments
    min_adjustment = -200
    max_adjustment = 200

    # Construct symbol with adjustments until it falls within the desired range
    while True:
        # Check if the symbol with boptions exists
        symbol_to_check = symbol + str(boptions) + option_type
        existing_positions = [position for position in broker.kite.positions()['net'] if position['tradingsymbol'] == symbol_to_check]

        if any(existing_positions):
            # Symbol with boptions exists, try adjustments
            for adjustment in range(min_adjustment, max_adjustment + 1, 100):
                adjusted_boptions = boptions + adjustment
                adjusted_symbol = symbol + str(adjusted_boptions) + option_type

                if not any(position for position in existing_positions if position['quantity'] > 0):
                    # Constructed symbol does not have existing positions with quantity > 0
                    return adjusted_symbol

        # No symbol with boptions found or adjustments didn't yield a suitable symbol, return default symbol
        return symbol + str(boptions) + option_type
def check_existing_positions(broker, symbol):
    positions_response = broker.kite.positions()
    positions_net = positions_response['net']
    for position in positions_net:
        if position['tradingsymbol'] == symbol and position['quantity'] > 0:
            return True
    return False
async def place_order(broker, symbol):
    try:
        order_id = broker.order_place(
            tradingsymbol=symbol,
            quantity=15,
            exchange="NFO",
            transaction_type='BUY',
            order_type='MARKET',
            product='NRML'
        )
        print(f"{symbol} is ordered")
        message_text = f"Option Order {symbol} placed successfully."
        await send_telegram_message(message_text)
        return True
    except Exception as e:
        print(f"Error placing Option order for {symbol}: {e}")
        return False
async def main():
    symbol = None
    try:
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
        sys.stdout = sys.__stdout__
    expiry_year, expiry_month = get_this_month_expiry()
    option_type = None
    if bmktpxy == 'Buy'and (smabank != 'below' or bnk_power < 0.05):
        option_type = 'CE'
    elif bmktpxy == 'Sell' and (smabank != 'above' or bnk_power > 0.95):
        option_type = 'PE'
    else:
        print("BNKTY - bmktpxy:", bmktpxy, "smabank:", smabank)
        sys.exit(0)
    symbol = construct_symbol(expiry_year, expiry_month, option_type, broker)
    if symbol is not None:
        if check_existing_positions(broker, symbol):
            print(f"{symbol} is already there")
        else:
            order_placed = await place_order(broker, symbol)
            if not order_placed:
                print("Order failed. Check error messages.")
async def run_main():
    await main()
asyncio.run(run_main())

