import yfinance as yf
import logging
from datetime import datetime
from login_get_kite import get_kite, remove_token
from cnstpxy import dir_path
import sys

# Initialize logging
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(message)s')

# Define the OI thresholds
OI_THRESHOLD_BANKNIFTY = 5000
OI_THRESHOLD_NIFTY = 10000

def get_current_price(symbol):
    try:
        data = yf.Ticker(symbol).history(period="1d", interval="1m")
        current_price = data['Close'].iloc[-1]
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
    next_month_abbr = datetime(next_year, next_month, 1).strftime('%b').upper()
    return f"{next_year % 100:02d}{next_month_abbr}"

def get_open_interest(symbol, kite):
    try:
        response = kite.ltp(f"NFO:{symbol}")
        oi = response[f"NFO:{symbol}"].get("oi")  # Assuming 'oi' is the open interest key
        return oi
    except Exception as e:
        logging.error(f"Error fetching open interest for {symbol}: {e}")
        return None

def get_cheapest_option_price(option_type, strike_price, kite, index_type='NIFTY'):
    strikes = [strike_price, strike_price + 100, strike_price - 100]
    cheapest_price = float('inf')
    cheapest_symbol = None

    next_month_str = get_next_month_str()

    for strike in strikes:
        if index_type == 'NIFTY':
            symbol = f"NIFTY{next_month_str}{strike:05d}{option_type}"
            oi_threshold = OI_THRESHOLD_NIFTY
        else:
            symbol = f"BANKNIFTY{next_month_str}{strike:05d}{option_type}"
            oi_threshold = OI_THRESHOLD_BANKNIFTY
        
        logging.info(f"Checking symbol: NFO:{symbol}")

        try:
            response = kite.ltp(f"NFO:{symbol}")
            ltp = response[f"NFO:{symbol}"]["last_price"]
            oi = get_open_interest(symbol, kite)
            if oi is not None and oi >= oi_threshold:
                if ltp < cheapest_price:
                    cheapest_price = ltp
                    cheapest_symbol = symbol
        except Exception as e:
            logging.error(f"Error fetching data for {symbol}: {e}")

    return cheapest_symbol, cheapest_price

def extract_strike_price(symbol):
    try:
        if 'BANKNIFTY' in symbol:
            parts = symbol.split('BANKNIFTY')[1]
        elif 'NIFTY' in symbol:
            parts = symbol.split('NIFTY')[1]
        else:
            raise ValueError("Symbol does not contain expected index")
    
        strike_price_str = parts[5:10]
        strike_price = int(strike_price_str)
        
        return strike_price
    except (ValueError, IndexError) as e:
        logging.error(f"Error extracting strike price from symbol '{symbol}': {e}")
        return None

def get_prices():
    try:
        with open('output.txt', 'w') as file:
            sys.stdout = file
            sys.stderr = file
            logging.basicConfig(stream=file, level=logging.ERROR)
    
            try:
                kite = get_kite()
            except Exception as e:
                remove_token(dir_path)
                logging.error(f"{str(e)} unable to get Kite instance")
                sys.exit(1)
    finally:
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__
    
    BCEX_Strike, CEX_Strike, PEX_Strike, BPEX_Strike = get_strikes()

    bce_symbol, bce_price = get_cheapest_option_price("CE", BCEX_Strike, kite, index_type='BANKNIFTY')
    bpe_symbol, bpe_price = get_cheapest_option_price("PE", BPEX_Strike, kite, index_type='BANKNIFTY')
    ce_symbol, ce_price = get_cheapest_option_price("CE", CEX_Strike, kite, index_type='NIFTY')
    pe_symbol, pe_price = get_cheapest_option_price("PE", PEX_Strike, kite, index_type='NIFTY')

    BCE_Strike = extract_strike_price(bce_symbol)
    CE_Strike = extract_strike_price(ce_symbol)
    PE_Strike = extract_strike_price(pe_symbol)
    BPE_Strike = extract_strike_price(bpe_symbol)

    return BCE_Strike, CE_Strike, PE_Strike, BPE_Strike

if __name__ == "__main__":
    try:
        prices = get_prices()
        print("Strike Prices:", prices)
    except Exception as e:
        logging.error(f"Unexpected error: {e}")

