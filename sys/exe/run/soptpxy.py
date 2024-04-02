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
from optpxy import get_opt_check
optpxy = get_opt_check('^NSEI')

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
    expiry_day = this_thursday.strftime("%d").zfill(2)
    return expiry_year, expiry_month, expiry_day

def construct_symbol(expiry_year, expiry_month, expiry_day, option_type):
    if expiry_day is None:
        return f"NIFTY{expiry_year}{expiry_month}{noptions + 50}{option_type}"
    else:
        return f"NIFTY{expiry_year}{expiry_month}{expiry_day}{noptions + 50}{option_type}"

def check_existing_positions(broker, symbol):
    positions_response = broker.kite.positions()
    positions_net = positions_response['net']
    for position in positions_net:
        # Check if 'tradingsymbol' matches and 'quantity' is at least 50
        if position['tradingsymbol'] == symbol and position['quantity'] < 1:
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
    
    expiry_year, expiry_month, expiry_day = get_this_thursday()
    option_type = 'CE'  
    symbol = construct_symbol(expiry_year, expiry_month, expiry_day, option_type)
    
    if check_existing_positions(broker, symbol):
        print(f"Existing order for {symbol} found. Skipping order placement.")
        return
    
    # Place SELL order with MIS product type
    sell_order_placed, sell_order_id = await place_order(broker, symbol, 'SELL', 'MIS', 50, 'MARKET')
    if sell_order_placed:
        print("SELL order placed successfully.")
        
        # Get executed price
        order_history = broker.kite.order_history(sell_order_id)
        print("Order History:", order_history)  # Print order history to understand its structure
        
        if isinstance(order_history, list) and order_history:
            executed_price = order_history[-1]['average_price']  # Accessing 'average_price' from the last element
            if executed_price > 0:
                # Calculate target price (94% of executed price) and round to one decimal place
                target_price = round(executed_price - 7, 1)
                # Place BUY order with MIS product type at target price
                buy_order_placed, buy_order_id = await place_order(broker, symbol, 'BUY', 'MIS', 50, 'LIMIT', price=target_price)
                if buy_order_placed:
                    print("BUY order placed successfully at target price:", target_price)
            else:
                print("Error: Executed price is zero or negative.")
        else:
            print("Error: Unable to retrieve order history or empty history.")

async def run_main():
    await main()

asyncio.run(run_main())
