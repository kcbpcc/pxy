import traceback
import sys
import logging
from kiteconnect import KiteConnect
from login_get_kite import get_kite, remove_token
from cnstpxy import dir_path
from predictpxy import predict_market_sentiment

# Import color constants
from clorpxy import SILVER, UNDERLINE, RED, GREEN, YELLOW, RESET, BRIGHT_YELLOW, BRIGHT_RED, BRIGHT_GREEN, BOLD, GREY

# Define month abbreviations
MONTH_ABBR = {
    "01": "JAN",
    "02": "FEB",
    "03": "MAR",
    "04": "APR",
    "05": "MAY",
    "06": "JUN",
    "07": "JUL",
    "08": "AUG",
    "09": "SEP",
    "10": "OCT",
    "11": "NOV",
    "12": "DEC"
}

# Configure logging
logging.basicConfig(filename='debug.log', level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def construct_symbols(expiry_year, expiry_month, option_type, strike_price):
    # Convert expiry_month to abbreviation
    expiry_month_abbr = MONTH_ABBR.get(expiry_month, expiry_month)
    
    symbols = []
    if option_type == "CE":
        symbols.append(f"NIFTY{expiry_year}{expiry_month_abbr}{strike_price}CE")
        symbols.append(f"NIFTY{expiry_year}{expiry_month_abbr}{strike_price + 100}CE")
        symbols.append(f"NIFTY{expiry_year}{expiry_month_abbr}{strike_price + 200}CE")
    elif option_type == "PE":
        symbols.append(f"NIFTY{expiry_year}{expiry_month_abbr}{strike_price}PE")
        symbols.append(f"NIFTY{expiry_year}{expiry_month_abbr}{strike_price - 100}PE")
        symbols.append(f"NIFTY{expiry_year}{expiry_month_abbr}{strike_price - 200}PE")
    return symbols

def get_option_prices(symbols, kite):
    prices = {}
    for symbol in symbols:
        try:
            # Fetch the LTP (Last Traded Price) for the symbol
            response = kite.ltp(f"NFO:{symbol}")
            ltp = response[f"NFO:{symbol}"]["last_price"]
            prices[symbol] = ltp
            logging.debug(f"Fetched price for {symbol}: {ltp}")
        except Exception as e:
            logging.error(f"Error fetching price for {symbol}: {e}")
            prices[symbol] = float('inf')  # Set to infinity if price fetch fails
    return prices

def find_cheapest_symbol(prices):
    # Find the symbol with the lowest price
    cheapest_symbol = min(prices, key=prices.get)
    return cheapest_symbol

def main():
    try:
        # Redirect sys.stdout to 'output.txt'
        with open('output.txt', 'w') as file:
            sys.stdout = file

            try:
                # Log in to Kite Connect
                kite = get_kite()
                logging.info("Successfully logged in to Kite Connect.")
            except Exception as e:
                # If login fails, remove token and log the error
                logging.error(f"Failed to log in to Kite Connect: {e}")
                remove_token(dir_path)
                print(traceback.format_exc())
                sys.exit(1)

            # Define your parameters
            expiry_year = "24"
            expiry_month = "08"  # August
            option_type = "CE"
            strike_price = 25000  # Updated strike price

            # Construct symbols and get their prices
            symbols = construct_symbols(expiry_year, expiry_month, option_type, strike_price)
            logging.info(f"Constructed symbols: {symbols}")
            
            prices = get_option_prices(symbols, kite)
            logging.info(f"Option prices: {prices}")

            # Find the cheapest symbol
            cheapest_symbol = find_cheapest_symbol(prices)
            logging.info(f"The cheapest symbol is: {cheapest_symbol}")
            print(f"The cheapest symbol is: {cheapest_symbol}")

    finally:
        # Reset sys.stdout to its default value
        sys.stdout = sys.__stdout__

if __name__ == "__main__":
    main()

