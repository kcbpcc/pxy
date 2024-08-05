import yfinance as yf
import logging
from datetime import datetime
from login_get_kite import get_kite, remove_token
from cnstpxy import dir_path
import sys
import traceback

# Initialize logging
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(message)s')

def get_current_price(symbol):
    try:
        data = yf.Ticker(symbol).history(period="1d", interval="1m")  # Fetch only one day of data
        current_price = data['Close'].iloc[-1]  # Get the last available price
        return current_price
    except Exception as e:
        logging.error(f"Error fetching current price for {symbol}: {e}")
        return float('inf')

def round_to_nearest_100(price):
    return round(price / 100) * 100

def get_strikes():
    BCEX_Strike = round_to_nearest_100(get_current_price('^NSEBANK'))
    CEX_Strike = round_to_nearest_100(get_current_price('^NSEI'))
    PEX_Strike = round_to_nearest_100(get_current_price('^NSEI'))
    BPEX_Strike = round_to_nearest_100(get_current_price('^NSEBANK'))
    return BCEX_Strike, CEX_Strike, PEX_Strike, BPEX_Strike

def get_next_month_str():
    now = datetime.now()
    next_month = (now.month % 12) + 1
    next_year = now.year if next_month > 1 else now.year + 1
    
    # Convert next month to three-letter abbreviation
    next_month_abbr = datetime(next_year, next_month, 1).strftime('%b').upper()  # e.g., 'JAN', 'FEB'
    return f"{next_year % 100:02d}{next_month_abbr}"  # Format: YYMMM

def get_cheapest_option_price(option_type, strike_price, kite, index_type='NIFTY'):
    strikes = [strike_price, strike_price + 100, strike_price - 100]
    cheapest_price = float('inf')
    cheapest_symbol = None

    # Get next month and year
    next_month_str = get_next_month_str()

    for strike in strikes:
        if index_type == 'NIFTY':
            symbol = f"NIFTY{next_month_str}{strike:05d}{option_type}"
        else:
            symbol = f"BANKNIFTY{next_month_str}{strike:05d}{option_type}"
        
        logging.info(f"Checking symbol: NFO:{symbol}")
        print(f"Checking symbol: NFO:{symbol}")  # Debugging print

        try:
            response = kite.ltp(f"NFO:{symbol}")
            ltp = response[f"NFO:{symbol}"]["last_price"]
            print(f"Price for {symbol}: {ltp}")  # Debugging print
            if ltp < cheapest_price:
                cheapest_price = ltp
                cheapest_symbol = symbol
        except Exception as e:
            logging.error(f"Error fetching price for {symbol}: {e}")

    return cheapest_symbol, cheapest_price

def extract_strike_price(symbol):
    try:
        # Split the symbol to isolate the strike price part
        if 'BANKNIFTY' in symbol:
            parts = symbol.split('BANKNIFTY')[1]
        elif 'NIFTY' in symbol:
            parts = symbol.split('NIFTY')[1]
        else:
            raise ValueError("Symbol does not contain expected index")
    
        # The strike price is expected to be the 5-digit number before 'CE' or 'PE'
        strike_price_str = parts[5:10]
        strike_price = int(strike_price_str)
        
        return strike_price
    except (ValueError, IndexError) as e:
        logging.error(f"Error extracting strike price from symbol '{symbol}': {e}")
        return None

def get_prices():
    # Initialize Kite API
    try:
        kite = get_kite()
    except Exception as e:
        remove_token(dir_path)
        logging.error(f"{str(e)} unable to get Kite instance")
        sys.exit(1)
    
    # Get the strike prices for options
    BCEX_Strike, CEX_Strike, PEX_Strike, BPEX_Strike = get_strikes()

    # For BankNifty options
    bce_symbol, bce_price = get_cheapest_option_price("CE", BCEX_Strike, kite, index_type='BANKNIFTY')
    bpe_symbol, bpe_price = get_cheapest_option_price("PE", BPEX_Strike, kite, index_type='BANKNIFTY')

    # For Nifty options
    ce_symbol, ce_price = get_cheapest_option_price("CE", CEX_Strike, kite, index_type='NIFTY')
    pe_symbol, pe_price = get_cheapest_option_price("PE", PEX_Strike, kite, index_type='NIFTY')

    #print(f"BCE Strike: {BCEX_Strike}, Cheapest BCE: Symbol={bce_symbol}, Price={bce_price}")
    #print(f"CE Strike: {CEX_Strike}, Cheapest CE: Symbol={ce_symbol}, Price={ce_price}")
    #print(f"PE Strike: {PEX_Strike}, Cheapest PE: Symbol={pe_symbol}, Price={pe_price}")
    #print(f"BPE Strike: {BPEX_Strike}, Cheapest BPE: Symbol={bpe_symbol}, Price={bpe_price}")

    # Extracting the strike prices from the symbols
    BCE_Strike = extract_strike_price(bce_symbol)
    CE_Strike = extract_strike_price(ce_symbol)
    PE_Strike = extract_strike_price(pe_symbol)
    BPE_Strike = extract_strike_price(bpe_symbol)

    return BCE_Strike, CE_Strike, PE_Strike, BPE_Strike
