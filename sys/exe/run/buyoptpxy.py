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
noptions, _, _, _ = get_prices()
from macdpxy import calculate_macd_signal
from smapxy import check_index_status
nsma = check_index_status('^NSEI')
from mktpxy import get_market_check
onemincandlesequance, mktpxy = get_market_check('^NSEI')

async def send_telegram_message(message_text):
    try:
        # Define the bot token and your Telegram username or ID
        bot_token = '6867988078:AAGNBJqs4Rf8MR4xPGoL1-PqDOYouPan7b0'  # Replace with your actual bot token
        user_usernames = '-4136531362'  # Replace with your Telegram username or ID
        # Create a Telegram bot
        bot = telegram.Bot(token=bot_token)
        # Send the message to Telegram
        await bot.send_message(chat_id=user_usernames, text=message_text)
    except Exception as e:
        # Handle the exception (e.g., log it) and continue with your code
        print(f"Error sending message to Telegram: {e}")

# Define function to get this week's Thursday date
from datetime import datetime, timedelta
def get_this_thursday():
    current_date = datetime.now()
    days_until_this_thursday = (3 - current_date.weekday() + 7) % 7
    if days_until_this_thursday == 0:
        return current_date.strftime("%y"), current_date.strftime("%m"), current_date.strftime("%d").zfill(2)
    this_thursday = current_date + timedelta(days=days_until_this_thursday)
    last_day_of_month = (this_thursday.replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)
    if this_thursday.month != (this_thursday + timedelta(days=7)).month:
        if this_thursday.day > last_day_of_month.day - 7:
            return this_thursday.strftime("%y"), this_thursday.strftime("%m"), this_thursday.strftime("%d").zfill(2)
    expiry_year = this_thursday.strftime("%y")
    month_number = int(this_thursday.strftime("%m"))
    expiry_month = str(month_number) if month_number <= 9 else this_thursday.strftime("%m")
    expiry_day_adjest = timedelta(days=adjest)  # Example adjustment of 7 days
    expiry_day = (this_thursday - expiry_day_adjest).strftime("%d").zfill(2)
    return expiry_year, expiry_month, expiry_day

def construct_symbol(expiry_year, expiry_month, expiry_day, option_type):
    # Convert expiry_month to a single digit string if it's less than or equal to 9
    if len(expiry_month) == 2 and expiry_month.startswith("0"):
        expiry_month = expiry_month[1]

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
    #print(f"Debug: CE positions: {count_CE}, PE positions: {count_PE}")

    print(f"🔥CE positions:{count_CE}   ⚖️⚖️   PE positions:{count_PE}💧")

    PE_weight = count_PE - count_CE
    CE_weight = count_CE - count_PE
    weight = abs(count_PE - count_CE)
    #print(f"Debug: PE_weight: {PE_weight}, CE_weight: {CE_weight}, weight: {weight}")
    
    expiry_year, expiry_month, expiry_day = get_this_thursday()
    #print(f"Debug: Expiry Date - Year: {expiry_year}, Month: {expiry_month}, Day: {expiry_day}")

    option_type = 'CE' if (mktpxy == 'Buy' and CE_weight < 1) else ('PE' if (mktpxy == 'Sell' and PE_weight < 1) else (print(f"Market-{mktpxy} and Weight:{weight} - let's wait 🔍👀") or sys.exit(1)))
    #print(f"Debug: Option type: {option_type}")

    symbol = construct_symbol(expiry_year, expiry_month, expiry_day, option_type)
    #print(f"Debug: Symbol: {symbol}")

    position_exists = check_existing_positions(broker, symbol)
    #print(f"Debug: Position exists: {position_exists}")

    if not position_exists:
        buy_order_placed, buy_order_id = await place_order(broker, symbol, 'BUY', 'NRML', 50, 'MARKET')
        if buy_order_placed:
            await send_telegram_message(f"{symbol} BUY order placed successfully.")
            print(f"{symbol} BUY order placed successfully.")
    else:
        print(f"Existing {symbol}, So not buying")

async def run_main():
    await main()

asyncio.run(run_main())
