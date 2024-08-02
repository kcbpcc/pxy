import traceback
import sys
import logging
from kiteconnect import KiteConnect
from login_get_kite import get_kite, remove_token
from cnstpxy import dir_path
from predictpxy import predict_market_sentiment

# Import color constants
from clorpxy import SILVER, UNDERLINE, RED, GREEN, YELLOW, RESET, BRIGHT_YELLOW, BRIGHT_RED, BRIGHT_GREEN, BOLD, GREY

# Initialize constants
mktpredict = predict_market_sentiment()

def construct_symbols(expiry_year, expiry_month, option_type, strike_price):
    symbols = []
    if option_type == "CE":
        symbols.append(f"NIFTY{expiry_year}{expiry_month}{strike_price}CE")
        symbols.append(f"NIFTY{expiry_year}{expiry_month}{strike_price + 100}CE")
        symbols.append(f"NIFTY{expiry_year}{expiry_month}{strike_price + 200}CE")
    elif option_type == "PE":
        symbols.append(f"NIFTY{expiry_year}{expiry_month}{strike_price}PE")
        symbols.append(f"NIFTY{expiry_year}{expiry_month}{strike_price - 100}PE")
        symbols.append(f"NIFTY{expiry_year}{expiry_month}{strike_price - 200}PE")
    return symbols

def get_option_prices(symbols, kite):
    prices = {}
    for symbol in symbols:
        try:
            # Fetch the LTP (Last Traded Price) for the symbol
            ltp = kite.ltp(f"NFO:{symbol}")["NFO:{symbol}"]["last_price"]
            prices[symbol] = ltp
        except Exception as e:
            print(f"Error fetching price for {symbol}: {e}")
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
            except Exception as e:
                # If login fails, remove token and log the error
                remove_token(dir_path)
                print(traceback.format_exc())
                logging.error(f"{str(e)} unable to log in to Kite Connect")
                sys.exit(1)

            # Define your parameters
            expiry_year = "24"
            expiry_month = "08"
            option_type = "CE"
            strike_price = 25000  # Updated strike price

            # Construct symbols and get their prices
            symbols = construct_symbols(expiry_year, expiry_month, option_type, strike_price)
            prices = get_option_prices(symbols, kite)

            # Find the cheapest symbol
            cheapest_symbol = find_cheapest_symbol(prices)
            print(f"The cheapest symbol is: {cheapest_symbol}")

    finally:
        # Reset sys.stdout to its default value
        sys.stdout = sys.__stdout__

if __name__ == "__main__":
    main()

