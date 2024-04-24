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


def construct_symbol(expiry_year, expiry_month, expiry_day, option_type, strike):
    if len(expiry_month) == 2 and expiry_month.startswith("0"):
        expiry_month = expiry_month[1]

    if expiry_day is None:
        return f"NIFTY{expiry_year}{expiry_month}{strike}{option_type}"
    else:
        return f"NIFTY{expiry_year}{expiry_month}{expiry_day}{strike}{option_type}"


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
        with open('output.txt', 'w') as file:
            sys.stdout = file

            try:
                broker = get_kite(api="bypass", sec_dir=dir_path)
            except Exception as e:
                remove_token(dir_path)
                print(traceback.format_exc())
                logging.error(f"{str(e)} unable to get holdings")
                await send_telegram_message(f"Error: {str(e)}. Unable to get holdings.")
                return  # Exit the function if unable to get the broker

    finally:
        sys.stdout = sys.__stdout__
    
    expiry_year, expiry_month, expiry_day = get_this_thursday()
    
    # Define strike prices for call and put options
    call_strike = noptions - 200  # Example: Adding 200 points to the price for the call option
    put_strike = noptions + 200   # Example: Subtracting 200 points from the price for the put option
    
    # Construct symbols for call and put options with the respective strike prices
    ce_option_type = 'CE'
    pe_option_type = 'PE'
    ce_symbol = construct_symbol(expiry_year, expiry_month, expiry_day, ce_option_type, call_strike)
    pe_symbol = construct_symbol(expiry_year, expiry_month, expiry_day, pe_option_type, put_strike)
    
    # Check if there are existing positions for CE and PE options with quantity >= 50
    ce_position_exists = check_existing_positions(broker, ce_symbol)
    pe_position_exists = check_existing_positions(broker, pe_symbol)
    
    if not ce_position_exists:
        # Place BUY order for CE option
        buy_order_placed_ce, buy_order_id_ce = await place_order(broker, ce_symbol, 'BUY', 'NRML', 50, 'MARKET')
        if buy_order_placed_ce:
            print("BUY order for CE placed successfully.")
    else:
         print(f"Existing {ce_symbol}, So not Buying")
    
    if not pe_position_exists:
        # Place BUY order for PE option
        buy_order_placed_pe, buy_order_id_pe = await place_order(broker, pe_symbol, 'BUY', 'NRML', 50, 'MARKET')
        if buy_order_placed_pe:
            print("BUY order for PE placed successfully.")
    else:
         print(f"Existing {pe_symbol}, So not Buying")

async def run_main():
    await main()

asyncio.run(run_main())
