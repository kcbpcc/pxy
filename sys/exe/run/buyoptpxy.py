#buyoptpxy.py
adjest = 0
import traceback
import sys
import logging
import telegram
import asyncio
from login_get_kite import get_kite, remove_token
from cnstpxy import dir_path
from strikpxy import get_prices
_, CE_Strike, PE_Strike, _ = get_prices()
from macdpxy import calculate_macd_signal
from smapxy import check_index_status
nsma = check_index_status('^NSEI')
from mktpxy import get_market_check
onemincandlesequance, mktpxy = get_market_check('^NSEI')
from datetime import datetime, timedelta
from clorpxy import SILVER, UNDERLINE, RED, GREEN, YELLOW, RESET, BRIGHT_YELLOW, BRIGHT_RED, BRIGHT_GREEN, BOLD, GREY
print("━" * 42)
async def send_telegram_message(message_text):
    try:
        # Define the bot token and your Telegram username or ID
        bot_token = '7141714085:AAHlyEzszCy9N-L6wO1zSAkRwGdl0VTQCFI'  # Replace with your actual bot token
        user_usernames = '-4128494197'  # Replace with your Telegram username or ID
        # Create a Telegram bot
        bot = telegram.Bot(token=bot_token)
        # Send the message to Telegram
        await bot.send_message(chat_id=user_usernames, text=message_text)
    except Exception as e:
        # Handle the exception (e.g., log it) and continue with your code
        print(f"Error sending message to Telegram: {e}")

# Define function to get this week's Thursday date

from datetime import datetime, timedelta

def get_this_thursday(adjest=7):
    current_date = datetime.now()
    days_until_this_thursday = (3 - current_date.weekday() + 7) % 7
    if days_until_this_thursday == 0:
        expiry_year = current_date.strftime("%y")
        expiry_month = current_date.strftime("%b").upper()  # Convert to all caps
        expiry_day = current_date.strftime("%d").zfill(2)
        return expiry_year, expiry_month, expiry_day
    this_thursday = current_date + timedelta(days=days_until_this_thursday)
    last_day_of_month = (this_thursday.replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)
    if this_thursday.month != (this_thursday + timedelta(days=7)).month:
        if this_thursday.day > last_day_of_month.day - 7:
            expiry_year = this_thursday.strftime("%y")
            expiry_month = this_thursday.strftime("%b").upper()  # Convert to all caps
            expiry_day = ''  # Empty day
            return expiry_year, expiry_month, expiry_day
    expiry_year = this_thursday.strftime("%y")
    expiry_month = this_thursday.strftime("%b").upper()  # Convert to all caps
    expiry_day_adjust = timedelta(days=adjest)  # Adjustment of days
    expiry_day = (this_thursday - expiry_day_adjust).strftime("%d").zfill(2)
    return expiry_year, expiry_month, expiry_day

def construct_symbol(expiry_year, expiry_month, expiry_day, option_type):
    # Convert expiry_month to a single digit string if it's less than or equal to 9
    if len(expiry_month) == 2 and expiry_month.startswith("0"):
        expiry_month = expiry_month[1]
    noptions = PE_Strike if option_type == "PE" else (CE_Strike if option_type == "CE" else None)
    if expiry_day is None:
        return f"NIFTY{expiry_year}{expiry_month}{noptions}{option_type}"
    else:
        return f"NIFTY{expiry_year}{expiry_month}{expiry_day}{noptions}{option_type}"

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
        # Reset sys.stdout to its default value
        sys.stdout = sys.__stdout__
    
    count_CE, count_PE = count_positions_by_type(broker)
    PE_weight = count_PE - count_CE
    CE_weight = count_CE - count_PE
    weight = abs(count_PE - count_CE)

    print(f"{BRIGHT_YELLOW}🔥CE positions:{count_CE} 📈━{weight}━📉 PE positions:{count_PE}💧{RESET}".rjust(42))

    expiry_year, expiry_month, expiry_day = get_this_thursday()

    option_type = 'CE' if (mktpxy == 'Buy' and CE_weight < 1 and count_CE < 4) else ('PE' if (mktpxy == 'Sell' and PE_weight < 1 and count_PE < 4) else (print(f"Market-{mktpxy} or Unbalanced-let's wait 🔍👀".rjust(39))) or sys.exit(1))
    symbol = construct_symbol(expiry_year, expiry_month, expiry_day, option_type)

    position_exists = check_existing_positions(broker, symbol)
    
    if not position_exists:
        # await the coroutine
        buy_order_placed, buy_order_id = await place_order(broker, symbol, 'BUY', 'NRML', 50, 'MARKET')
        if buy_order_placed:
            # Send Telegram message
            send_telegram_message(f"🛫🛫🛫 👉👉👉 ENTRY order placed for {symbol} placed successfully.")
            print(f"{symbol} BUY order placed successfully.")
    else:
        print(f"Existing {symbol}, So not buying")

async def run_main():
    await main()

await run_main()
