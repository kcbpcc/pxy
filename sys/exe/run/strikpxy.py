import yfinance as yf
import logging
from datetime import datetime, timedelta
import calendar

# Function to get current price of a given symbol
def get_current_price(symbol):
    try:
        data = yf.Ticker(symbol).history(period="1d", interval="1m")  # Fetch only one day of data
        current_price = data['Close'].iloc[-1]  # Get the last available price
        return current_price
    except Exception as e:
        logging.error(f"Error fetching data for symbol {symbol}: {e}")
        return float('inf')  # Return infinity if there's an error

# Function to get the abbreviation of the next month
def get_next_month_abbr():
    today = datetime.now()
    next_month = (today.month % 12) + 1
    next_month_name = calendar.month_abbr[next_month]
    return next_month_name.upper()

# Function to round price to the nearest 100
def round_to_nearest_100(price):
    return round(price / 100) * 100

# Function to round price to the nearest 200
def round_to_nearest_200(price):
    return round(price / 200) * 200

# Function to round price to the nearest 50 or 100
def round_to_nearest_50_or_100(price):
    return round(price / 50) * 50 if price % 100 < 50 else round(price / 100) * 100

# Function to get the strike prices and their corresponding symbols
def get_strikes():
    BCE_Strike = round_to_nearest_100(get_current_price('^NSEBANK'))
    CE_Strike = round_to_nearest_100(get_current_price('^NSEI'))
    PE_Strike = round_to_nearest_100(get_current_price('^NSEI'))
    BPE_Strike = round_to_nearest_100(get_current_price('^NSEBANK'))
    return BCE_Strike, CE_Strike, PE_Strike, BPE_Strike

# Function to get the symbol with the cheapest price for given strikes
def get_cheapest_option_price(symbol_type, strike, kite, month_abbr):
    min_price = float('inf')
    best_symbol = None
    for offset in [-100, 0, 100]:
        option_strike = strike + offset
        option_symbol = f"{symbol_type}{expiry_year}{month_abbr}{option_strike:05d}{symbol_type}"
        logging.info(f"Checking symbol: {option_symbol}")
        price = kite.get_price(option_symbol)
        if price < min_price:
            min_price = price
            best_symbol = option_symbol
    return best_symbol, min_price

# Function to print the cheapest prices for all options
def print_cheapest_prices(kite):
    month_abbr = get_next_month_abbr()
    expiry_year = datetime.now().strftime("%y")  # Get current year in 2-digit format

    BCE_Strike, CE_Strike, PE_Strike, BPE_Strike = get_strikes()

    bce_symbol, bce_price = get_cheapest_option_price("BANKNIFTY", BCE_Strike, kite, month_abbr)
    ce_symbol, ce_price = get_cheapest_option_price("NIFTY", CE_Strike, kite, month_abbr)
    pe_symbol, pe_price = get_cheapest_option_price("NIFTY", PE_Strike, kite, month_abbr)
    bpe_symbol, bpe_price = get_cheapest_option_price("BANKNIFTY", BPE_Strike, kite, month_abbr)

    print(f"BCE Strike: {BCE_Strike}, Cheapest BCE: Symbol={bce_symbol}, Price={bce_price}")
    print(f"CE Strike: {CE_Strike}, Cheapest CE: Symbol={ce_symbol}, Price={ce_price}")
    print(f"PE Strike: {PE_Strike}, Cheapest PE: Symbol={pe_symbol}, Price={pe_price}")
    print(f"BPE Strike: {BPE_Strike}, Cheapest BPE: Symbol={bpe_symbol}, Price={bpe_price}")

# Assuming `kite` is initialized somewhere else in your script
# print_cheapest_prices(kite)
