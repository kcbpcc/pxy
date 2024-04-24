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
from thudaypxy import get_this_thursday
expiry_year, expiry_month, expiry_day = get_this_thursday()

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

def construct_symbol(expiry_year, expiry_month, expiry_day, option_type):
    # Convert expiry_month to a single digit string if it's less than or equal to 9
    if len(expiry_month) == 2 and expiry_month.startswith("0"):
        expiry_month = expiry_month[1]

    if expiry_day is None:
        return f"NIFTY{expiry_year}{expiry_month}{noptions - 100}{option_type}"
    else:
        return f"NIFTY{expiry_year}{expiry_month}{expiry_day}{noptions - 100}{option_type}"


def check_existing_positions(broker, symbol):
    positions_response = broker.kite.positions()
    positions_net = positions_response['net']
    for position in positions_net:
        if position['tradingsymbol'] == symbol and position['quantity'] < -300:
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
                target_price = round(executed_price - 10, 1)
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
