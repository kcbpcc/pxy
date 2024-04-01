from datetime import datetime, timedelta
import asyncio
import traceback
import sys
from logoptpxy import setup_logging, handle_order_placement_error
from teloptpxy import send_telegram_message
from login_get_kite import get_kite, remove_token
from cnstpxy import dir_path
from strikpxy import get_prices
from thuoptpxy import get_this_thursday, construct_symbol
from chkoptpxy import check_existing_positions
from ordoptpxy import place_order


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
                handle_order_placement_error('Getting Kite', e)
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
        executed_price = broker.kite.order_history(sell_order_id)['average_price']
        # Calculate target price (94% of executed price)
        target_price = executed_price * 0.94
        # Place BUY order with MIS product type at target price
        buy_order_placed, buy_order_id = await place_order(broker, symbol, 'BUY', 'MIS', 50, 'LIMIT', price=target_price)
        if buy_order_placed:
            print("BUY order placed successfully at target price:", target_price)

async def run_main():
    await main()

asyncio.run(run_main())
