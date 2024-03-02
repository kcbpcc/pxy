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
    found_positions = False
    positions_response = broker.kite.positions()
    positions_net = positions_response['net']
    open_positions_count = 0  # Counter to keep track of open positions with the same option_type
    for position in positions_net:
        if position['tradingsymbol'] == symbol + str(boptions) + option_type and position['quantity'] > 0:
            found_positions = True
            break
        if position['tradingsymbol'].startswith('BANKNIFTY') and position['tradingsymbol'].endswith(option_type) and position['quantity'] > 0:
            open_positions_count += 1
    # Check if there are already three open positions with the same option_type
    if open_positions_count >= 3:
        print(f"Hey! ...you have 3 {option_type} open positions.")
        return None  # Return None if three positions with the same option_type are already open
    if not found_positions:
        return f"{symbol}{boptions}{option_type}"
    adjustments = [100, -100, 200, -200]
    for adjustment in adjustments:
        adjusted_boptions = boptions + adjustment
        
        for position in positions:
            if position['tradingsymbol'] == symbol + str(adjusted_boptions) + option_type :
                return f"{symbol}{adjusted_boptions}{option_type}"
    return f"{symbol}{boptions}{option_type}"
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

