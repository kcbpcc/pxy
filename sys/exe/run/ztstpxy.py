import sys
import traceback
import logging

# Configure logging
logging.basicConfig(filename='error.log', level=logging.ERROR)

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

def construct_symbol(expiry_year, expiry_month, expiry_day, option_type, option_chain, strike_price):
    """Construct the symbol based on the average price of PE and CE options."""
    original_stdout = sys.stdout
    
    try:
        with open('output.txt', 'w') as file:
            sys.stdout = file
            try:
                expiry_month = expiry_month.lstrip("0")
                
                pe_price, ce_price = get_option_prices(strike_price)
                
                if pe_price is None or ce_price is None:
                    raise ValueError("Could not retrieve prices for the given strike price.")
                
                average_price = (pe_price + ce_price) / 2
                
                nearest_strike = get_nearest_strike_price(option_chain, average_price)
                
                # Example values for BPE_Strike and BCE_Strike
                BPE_Strike = 10000  # Replace with actual value
                BCE_Strike = 10000  # Replace with actual value
                noptions = BPE_Strike if option_type == "PE" else (BCE_Strike if option_type == "CE" else None)
                
                if expiry_day is None:
                    symbol = f"NIFTY{expiry_year}{expiry_month}{nearest_strike}{option_type}"
                else:
                    symbol = f"NIFTY{expiry_year}{expiry_month}{expiry_day}{nearest_strike}{option_type}"
                
                print(f"Constructed Symbol: {symbol}")
                
            except Exception as e:
                logging.error(f"{str(e)} unable to construct symbol")
                print(traceback.format_exc())
                sys.exit(1)
    finally:
        sys.stdout = original_stdout

    return symbol

def remove_token(dir_path):
    """Remove the token from the specified directory path."""
    # Placeholder for the actual function to remove the token
    pass

# Main function to prompt user input
def main():
    try:
        expiry_year = input("Enter expiry year (e.g., 2024): ")
        expiry_month = input("Enter expiry month (e.g., 07): ")
        expiry_day = input("Enter expiry day (e.g., 26, or leave blank if not applicable): ")
        option_type = input("Enter option type (PE/CE): ").upper()
        
        option_chain = [15000, 15500, 16000, 16500, 17000]  # Example strikes
        strike_price = int(input("Enter strike price: "))
        
        # Construct the symbol
        symbol = construct_symbol(expiry_year, expiry_month, expiry_day, option_type, option_chain, strike_price)
        print(f"Constructed Symbol: {symbol}")
    
    except Exception as e:
        logging.error(f"Error in main function: {str(e)}")
        print(traceback.format_exc())
        sys.exit(1)

if __name__ == "__main__":
    main()

