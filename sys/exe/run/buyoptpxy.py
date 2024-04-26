import traceback
import sys
import logging
import telegram
import asyncio
from login_get_kite import get_kite, remove_token
from cnstpxy import dir_path
from strikpxy import get_prices
from macdpxy import calculate_macd_signal
from smapxy import check_index_status
from mktpxy import get_market_check
from datetime import datetime, timedelta
from clorpxy import BRIGHT_YELLOW, RESET

_, CE_Strike, PE_Strike, _ = get_prices()
nsma = check_index_status('^NSEI')
onemincandlesequance, mktpxy = get_market_check('^NSEI')

async def send_telegram_message(message_text):
    try:
        bot_token = '7141714085:AAHlyEzszCy9N-L6wO1zSAkRwGdl0VTQCFI'
        user_usernames = '-4128494197'
        bot = telegram.Bot(token=bot_token)
        await bot.send_message(chat_id=user_usernames, text=message_text)
    except Exception as e:
        print(f"Error sending message to Telegram: {e}")

def last_thursday_of_month(year, month):
    last_day_of_month = datetime(year, month, 1) + timedelta(days=32)
    last_day_of_month = last_day_of_month.replace(day=1) - timedelta(days=1)
    last_thursday = last_day_of_month - timedelta(days=(last_day_of_month.weekday() + 1) % 7)
    return last_thursday

def get_expiry_date():
    current_date = datetime.now()
    next_month = current_date.month + 1 if current_date.month < 12 else 1
    next_year = current_date.year if current_date.month < 12 else current_date.year + 1
    expiry_date = last_thursday_of_month(next_year, next_month)
    return expiry_date.year, expiry_date.strftime("%b").upper()

def construct_symbol(expiry_year, expiry_month, option_type):
    if len(expiry_month) == 2 and expiry_month.startswith("0"):
        expiry_month = expiry_month[1]
    noptions = PE_Strike if option_type == "PE" else (CE_Strike if option_type == "CE" else None)
    return f"NIFTY{expiry_year}{expiry_month}{noptions}{option_type}"

def count_positions_by_type(broker):
    positions_response = broker.kite.positions()
    positions_net = positions_response['net']
    count_CE = 0
    count_PE = 0
    for position in positions_net:
        if position['tradingsymbol'].endswith('CE') and abs(position['quantity']) >= 50:
            count_CE += 1
        elif position['tradingsymbol'].endswith('PE') and abs(position['quantity']) >= 50:
            count_PE += 1
    return count_CE, count_PE

def check_existing_positions(broker, symbol):
    positions_response = broker.kite.positions()
    positions_net = positions_response['net']
    for position in positions_net:
        if position['tradingsymbol'] == symbol and abs(position['quantity']) >= 50:
            return True
    return False

async def place_order(broker, symbol, transaction_type, product_type, quantity, order_type, price=None):
    try:
        if price is None:
            order_id = broker.order_place(
                tradingsymbol=symbol,
                quantity=quantity,
                exchange="NFO",
                transaction_type=transaction_type,
                order_type=order_type,
                product=product_type
            )
        else:
            order_id = broker.order_place(
                tradingsymbol=symbol,
                quantity=quantity,
                exchange="NFO",
                transaction_type=transaction_type,
                order_type=order_type,
                product=product_type,
                price=price
            )
        return True, order_id
    except Exception as e:
        print(f"Error placing order for {symbol}: {e}")
        return False, None

async def main():
    try:
        broker = get_kite(api="bypass", sec_dir=dir_path)
    except Exception as e:
        remove_token(dir_path)
        print(traceback.format_exc())
        logging.error(f"{str(e)} unable to get holdings")
        sys.exit(1)
    
    count_CE, count_PE = count_positions_by_type(broker)
    PE_weight = count_PE - count_CE
    CE_weight = count_CE - count_PE
    weight = abs(count_PE - count_CE)

    expiry_year, expiry_month = get_expiry_date()

    option_type = 'CE' if (mktpxy == 'Bull' and CE_weight < 1 and count_CE < 4) else ('PE' if (mktpxy == 'Sell' and PE_weight < 1 and count_PE < 4) else (print(f"Market-{mktpxy} or Unbalanced-let's wait 🔍👀".rjust(39))) or sys.exit(1))
    symbol = construct_symbol(expiry_year, expiry_month, option_type)

    position_exists = check_existing_positions(broker, symbol)
    
    if not position_exists:
        buy_order_placed, buy_order_id = await place_order(broker, symbol, 'BUY', 'NRML', 50, 'MARKET')
        if buy_order_placed:
            await send_telegram_message(f"🛫🛫🛫 👉👉👉 ENTRY order placed for {symbol} placed successfully.")
            print(f"{symbol} BUY order placed successfully.")
    else:
        print(f"Existing {symbol}, So not buying")

async def run_main():
    await main()

asyncio.run(run_main())
