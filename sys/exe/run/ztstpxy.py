import sys
import traceback
import logging
from datetime import datetime, timedelta
from toolkit.logger import Logger
from login_get_kite import get_kite, remove_token
from cnstpxy import dir_path
from fundpxy import calculate_decision
import pandas as pd

# Configure logging
logging.basicConfig(level=logging.WARNING)
logging = Logger(30, dir_path + "main.log")

def get_ltp(exchange, tradingsymbol):
    """Fetch the last traded price (LTP) from the exchange."""
    key = f"{exchange}:{tradingsymbol}"
    try:
        resp = broker.kite.ltp(key)
        if resp and isinstance(resp, dict):
            return resp.get(key, {}).get('last_price', None)
    except Exception as e:
        logging.error(f"Error fetching LTP for {key}: {str(e)}")
    return None

def get_option_prices(strike_price):
    """Get PE and CE prices for the given strike price."""
    pe_symbol = f"NFO:{strike_price}PE"
    ce_symbol = f"NFO:{strike_price}CE"
    
    pe_price = get_ltp("NFO", pe_symbol)
    ce_price = get_ltp("NFO", ce_symbol)
    
    return pe_price, ce_price

def construct_symbol(strike_price):
    """Construct the symbol based on the current year and next month."""
    # Get the current date
    now = datetime.now()
    
    # Current year
    current_year = now.year
    
    # Next month
    next_month = (now.month % 12) + 1
    next_month_str = now.replace(day=1, month=next_month).strftime("%b").upper()
    
    # Format the expiry month
    expiry_month = next_month_str
    
    # Construct the symbol
    symbol = f"NIFTY{current_year}{expiry_month}{strike_price}"
    
    return symbol

def main():
    try:
        # Print initial info and cash available
        print("🍃🍃🍃 Lets Buy NIFTY VOLUME Stocks 🍃🍃🍃")
        decision, optdecision, available_cash, cash, limit = calculate_decision()
        print(f"     Cash:💰{available_cash:.2f}💵 | 🚦{decision}🚦 to Buy")
        
        # Redirect sys.stdout to 'output.txt' for broker initialization
        original_stdout = sys.stdout
        try:
            with open('output.txt', 'w') as file:
                sys.stdout = file
                try:
                    global broker
                    broker = get_kite()
                except Exception as e:
                    remove_token(dir_path)
                    print(traceback.format_exc())
                    logging.error(f"{str(e)} unable to get holdings")
                    sys.exit(1)
        finally:
            sys.stdout = original_stdout

        # Prompt user for strike price
        strike_price = input("Enter strike price: ")
        
        # Construct the symbol
        symbol = construct_symbol(strike_price)
        print(f"Constructed Symbol: {symbol}")

    except Exception as e:
        logging.error(f"Error in main function: {str(e)}")
        print(traceback.format_exc())
        sys.exit(1)

if __name__ == "__main__":
    main()

