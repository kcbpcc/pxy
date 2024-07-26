import sys
import traceback
import logging
from datetime import datetime
from toolkit.logger import Logger
from login_get_kite import get_kite, remove_token
from cnstpxy import dir_path
from fundpxy import calculate_decision

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

def get_nearest_strike_price(option_chain, target_price):
    """Find the nearest strike price in the option chain to the target price."""
    nearest_strike = None
    min_diff = float('inf')
    
    for strike in option_chain:
        diff = abs(strike - target_price)
        if diff < min_diff:
            min_diff = diff
            nearest_strike = strike
    
    return nearest_strike

def construct_symbol(strike_price, option_chain):
    """Construct the symbol based on the current year (2 digits) and next month."""
    # Get the current date
    now = datetime.now()
    
    # Two-digit year
    current_year = now.year % 100
    
    # Next month
    next_month = (now.month % 12) + 1
    next_month_str = now.replace(day=1, month=next_month).strftime("%b").upper()
    
    # Get PE and CE prices for the given strike
    pe_price, ce_price = get_option_prices(strike_price)
    
    if pe_price is None or ce_price is None:
        raise ValueError("Could not retrieve prices for the given strike price.")
    
    # Calculate average price
    average_price = (pe_price + ce_price) / 2
    
    # Find the nearest strike price in the option chain
    nearest_strike = get_nearest_strike_price(option_chain, average_price)
    
    # Construct the symbol
    symbol = f"NIFTY{current_year:02d}{next_month_str}{nearest_strike}"
    
    return symbol

def generate_option_chain(base_strike_price):
    """Generate a list of strike prices around the base strike price."""
    # Generate strikes every 100 below and above the base strike price
    option_chain = list(range(base_strike_price - 500, base_strike_price + 500 + 100, 100))
    return option_chain

def main():
    original_stdout = sys.stdout  # Save the original stdout

    try:
        # Redirect sys.stdout to 'output.txt' for broker initialization
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
        sys.stdout = original_stdout  # Ensure stdout is restored

    try:
        # Print initial info and cash available
        print("🍃🍃🍃 Lets Buy NIFTY VOLUME Stocks 🍃🍃🍃")
        decision, optdecision, available_cash,fdf, limit = calculate_decision()
        print(f"     Cash:💰{available_cash:.2f}💵 | 🚦{decision}🚦 to Buy")
        
        # Prompt user for strike price
        strike_price = int(input("Enter strike price: "))
        
        # Generate option chain dynamically
        option_chain = generate_option_chain(strike_price)
        
        # Construct the symbol
        symbol = construct_symbol(strike_price, option_chain)
        print(f"Constructed Symbol: {symbol}")

    except Exception as e:
        logging.error(f"Error in main function: {str(e)}")
        print(traceback.format_exc())
        sys.exit(1)

if __name__ == "__main__":
    main()

