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

def get_strikes():
    BCE_Strike = round_to_nearest_100(get_current_price('^NSEBANK'))
    CE_Strike = round_to_nearest_100(get_current_price('^NSEI'))
    PE_Strike = round_to_nearest_100(get_current_price('^NSEI'))
    BPE_Strike = round_to_nearest_100(get_current_price('^NSEBANK'))
    return BCE_Strike, CE_Strike, PE_Strike, BPE_Strike

def get_cheapest_option_price(symbol, strike_price, kite):
    strike_prices = [strike_price, strike_price + 100, strike_price - 100]
    cheapest_price = float('inf')
    cheapest_symbol = None
    
    for strike in strike_prices:
        option_symbol = f"BANKNIFTY{expiry_year}{expiry_month:02d}{strike:05d}{symbol}"
        
        try:
            response = kite.ltp(f"NFO:{option_symbol}")
            ltp = response[f"NFO:{option_symbol}"]["last_price"]
            
            if ltp < cheapest_price:
                cheapest_price = ltp
                cheapest_symbol = option_symbol
                
        except Exception as e:
            logging.error(f"Error fetching price for {option_symbol}: {e}")
    
    return cheapest_symbol, cheapest_price

def get_cheapest_prices(expiry_year, expiry_month, kite):
    BCE_Strike, CE_Strike, PE_Strike, BPE_Strike = get_strikes()
    
    ce_symbol, ce_price = get_cheapest_option_price("CE", CE_Strike, kite)
    pe_symbol, pe_price = get_cheapest_option_price("PE", PE_Strike, kite)
    bce_symbol, bce_price = get_cheapest_option_price("CE", BCE_Strike, kite)
    bpe_symbol, bpe_price = get_cheapest_option_price("PE", BPE_Strike, kite)
    
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

# Example usage
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

    # Define the expiry details
    expiry_year = "24"  # Example expiry year in YY format
    expiry_month = "08"  # Example expiry month in MM format

    # Get cheapest prices
    results = get_cheapest_prices(expiry_year, expiry_month, kite)
    
    # Print results
    print(f"BCE Strike: {results['BCE_Strike']}, Cheapest BCE: Symbol={results['Cheapest_BCE'][0]}, Price={results['Cheapest_BCE'][1]}")
    print(f"CE Strike: {results['CE_Strike']}, Cheapest CE: Symbol={results['Cheapest_CE'][0]}, Price={results['Cheapest_CE'][1]}")
    print(f"PE Strike: {results['PE_Strike']}, Cheapest PE: Symbol={results['Cheapest_PE'][0]}, Price={results['Cheapest_PE'][1]}")
    print(f"BPE Strike: {results['BPE_Strike']}, Cheapest BPE: Symbol={results['Cheapest_BPE'][0]}, Price={results['Cheapest_BPE'][1]}")


