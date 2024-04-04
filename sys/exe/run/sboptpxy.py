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

def construct_symbol(expiry_year, expiry_month, expiry_day, option_type, noptions):
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
        # Check if 'tradingsymbol' matches and 'quantity' is at least 50
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
    ce_option_type = 'CE'
    pe_option_type = 'PE'
    
    ce_symbol = construct_symbol(expiry_year, expiry_month, expiry_day, ce_option_type, noptions)
    pe_symbol = construct_symbol(expiry_year, expiry_month, expiry_day, pe_option_type, noptions)
    
    # Get available cash
    response = broker.kite.margins(segment="equity")
    available_cash = response["equity"]["available"]["live_balance"]
    print("Available Cash:", available_cash)
    
    # Get required margin for CE and PE
    ce_margin_required = get_required_margin(broker, ce_symbol)
    pe_margin_required = get_required_margin(broker, pe_symbol)
    
    if available_cash >= ce_margin_required + pe_margin_required:
        print("Funds are sufficient for both CE and PE options.")
    else:
        print("Funds are not sufficient for both CE and PE options. Exiting.")
        return
    
    if check_existing_positions(broker, ce_symbol) or check_existing_positions(broker, pe_symbol):
        print(f"Existing order for {ce_symbol} or {pe_symbol} found. Skipping order placement.")
        return
    
    # Place SELL order with MIS product type for CE and PE
    ce_sell_order_placed, ce_sell_order_id = await place_order(broker, ce_symbol, 'SELL', 'MIS', 50, 'MARKET')
    pe_sell_order_placed, pe_sell_order_id = await place_order(broker, pe_symbol, 'SELL', 'MIS', 50, 'MARKET')
    
    if ce_sell_order_placed and pe_sell_order_placed:
        print("SELL orders for CE and PE placed successfully.")
    else:
        print("Failed to place one or both SELL orders. Check logs for details.")

async def run_main():
    await main()

asyncio.run(run_main())
