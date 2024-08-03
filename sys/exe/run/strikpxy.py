import sys
import logging
import yfinance as yf
import warnings
from datetime import datetime
from login_get_kite import get_kite, remove_token
from cnstpxy import dir_path
from clorpxy import SILVER, UNDERLINE, RED, GREEN, YELLOW, RESET, BRIGHT_YELLOW, BRIGHT_RED, BRIGHT_GREEN, BOLD, GREY

# Suppress warnings
warnings.filterwarnings("ignore")

# Initialize logging
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(message)s')

def get_current_price(symbol):
    data = yf.Ticker(symbol).history(period="1d", interval="1m")  # Fetch only one day of data
    current_price = data['Close'].iloc[-1]  # Get the last available price
    return current_price

def round_to_nearest_100(price):
    return round(price / 100) * 100

def round_to_nearest_200(price):
    return round(price / 200) * 200

def round_to_nearest_100_or_50(price):
    return round(price / 50) * 50 if price % 100 < 50 else round(price / 100) * 100

def get_month_abbreviation(month_number):
    month_map = {
        1: 'JAN', 2: 'FEB', 3: 'MAR', 4: 'APR', 5: 'MAY', 6: 'JUN',
        7: 'JUL', 8: 'AUG', 9: 'SEP', 10: 'OCT', 11: 'NOV', 12: 'DEC'
    }
    return month_map.get(month_number, 'UNKNOWN')

def get_next_month_abbreviation():
    today = datetime.now()
    next_month = today.month % 12 + 1
    return get_month_abbreviation(next_month)

def get_strikes():
    BCE_Strike = round_to_nearest_100(get_current_price('^NSEBANK'))
    CE_Strike = round_to_nearest_100(get_current_price('^NSEI'))
    PE_Strike = round_to_nearest_100(get_current_price('^NSEI'))
    BPE_Strike = round_to_nearest_100(get_current_price('^NSEBANK'))
    return BCE_Strike, CE_Strike, PE_Strike, BPE_Strike

def get_cheapest_option_price(option_type, strike_price, expiry_year, expiry_month, kite):
    # Convert strike_price to integer
    strike_price = int(strike_price)
    strike_prices = [strike_price, strike_price + 100, strike_price - 100]
    cheapest_price = float('inf')
    cheapest_symbol = None
    
    expiry_month_abbr = get_month_abbreviation(expiry_month)

    for strike in strike_prices:
        option_symbol = f"BANKNIFTY{expiry_year}{expiry_month_abbr}{strike:05d}{option_type}"
        
        try:
            response = kite.ltp(f"NFO:{option_symbol}")
            ltp = response[f"NFO:{option_symbol}"]["last_price"]
            
            if ltp < cheapest_price:
                cheapest_price = ltp
                cheapest_symbol = option_symbol
                
        except Exception as e:
            logging.error(f"Error fetching price for {option_symbol}: {e}")
    
    return cheapest_symbol, cheapest_price

def get_cheapest_prices(kite):
    expiry_year = datetime.now().year % 100  # Get the current year in YY format
    expiry_month = get_next_month_abbreviation()
    BCE_Strike, CE_Strike, PE_Strike, BPE_Strike = get_strikes()
    
    ce_symbol, ce_price = get_cheapest_option_price("CE", CE_Strike, expiry_year, expiry_month, kite)
    pe_symbol, pe_price = get_cheapest_option_price("PE", PE_Strike, expiry_year, expiry_month, kite)
    bce_symbol, bce_price = get_cheapest_option_price("CE", BCE_Strike, expiry_year, expiry_month, kite)
    bpe_symbol, bpe_price = get_cheapest_option_price("PE", BPE_Strike, expiry_year, expiry_month, kite)
    
    return {
        "BCE_Strike": BCE_Strike,
        "CE_Strike": CE_Strike,
        "PE_Strike": PE_Strike,
        "BPE_Strike": BPE_Strike,
        "Cheapest_CE": (ce_symbol, ce_price),
        "Cheapest_PE": (pe_symbol, pe_price),
        "Cheapest_BCE": (bce_symbol, bce_price),
        "Cheapest_BPE": (bpe_symbol, bpe_price)
    }

def print_cheapest_prices(kite):
    results = get_cheapest_prices(kite)
    
    print(f"BCE Strike: {results['BCE_Strike']}, Cheapest BCE: Symbol={results['Cheapest_BCE'][0]}, Price={results['Cheapest_BCE'][1]}")
    print(f"CE Strike: {results['CE_Strike']}, Cheapest CE: Symbol={results['Cheapest_CE'][0]}, Price={results['Cheapest_CE'][1]}")
    print(f"PE Strike: {results['PE_Strike']}, Cheapest PE: Symbol={results['Cheapest_PE'][0]}, Price={results['Cheapest_PE'][1]}")
    print(f"BPE Strike: {results['BPE_Strike']}, Cheapest BPE: Symbol={results['Cheapest_BPE'][0]}, Price={results['Cheapest_BPE'][1]}")

    # Check if all strikes are available at a cheaper price
    strikes = {
        "BCE": results['Cheapest_BCE'],
        "CE": results['Cheapest_CE'],
        "PE": results['Cheapest_PE'],
        "BPE": results['Cheapest_BPE']
    }
    
    for key, (symbol, price) in strikes.items():
        current_price = get_current_price(symbol)
        if price < current_price:
            print(f"The {key} strike is available at a cheaper price: {symbol} at {price}")
        else:
            print(f"The {key} strike is not available at a cheaper price: {symbol} at {price}")

if __name__ == "__main__":
    # Redirect stdout to avoid printing broker information
    file = open('kite_log.txt', 'w')
    sys.stdout = file

    try:
        kite = get_kite()
    except Exception as e:
        remove_token(dir_path)
        logging.error(f"{str(e)} unable to get holdings")
        sys.exit(1)
    finally:
        # Reset sys.stdout to its default value
        sys.stdout = sys.__stdout__
        file.close()

    # Print cheapest prices
    print_cheapest_prices(kite)


