import yfinance as yf
import logging
from datetime import datetime
from login_get_kite import get_kite, remove_token
from cnstpxy import dir_path
import sys

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

def get_prices():
    def extract_strike(symbol):
        try:
            # Debugging print to see the symbol and the extracted part
            print(f"Extracting strike price from symbol: {symbol}")
            extracted_part = symbol[-8:-3]
            print(f"Extracted part for strike price: {extracted_part}")
            strike_price = int(extracted_part)
            return strike_price
        except (ValueError, IndexError) as e:
            logging.error(f"Error extracting strike price from symbol: {symbol}: {e}")
            return None

    global bce_symbol, ce_symbol, pe_symbol, bpe_symbol
    # Initialize these variables if not set
    bce_symbol, ce_symbol, pe_symbol, bpe_symbol = "", "", "", ""

    # Assuming these symbols are fetched from other functions and are available here
    BCE_Strike = extract_strike(bce_symbol)
    CE_Strike = extract_strike(ce_symbol)
    PE_Strike = extract_strike(pe_symbol)
    BPE_Strike = extract_strike(bpe_symbol)

    return BCE_Strike, CE_Strike, PE_Strike, BPE_Strike

def print_cheapest_prices(kite):
    global bce_symbol, ce_symbol, pe_symbol, bpe_symbol

    BCEX_Strike, CEX_Strike, PEX_Strike, BPEX_Strike = get_strikes()

    # For BankNifty options
    bce_symbol, bce_price = get_cheapest_option_price("CE", BCEX_Strike, kite, index_type='BANKNIFTY')
    bpe_symbol, bpe_price = get_cheapest_option_price("PE", BPEX_Strike, kite, index_type='BANKNIFTY')

    # For Nifty options
    ce_symbol, ce_price = get_cheapest_option_price("CE", CEX_Strike, kite, index_type='NIFTY')
    pe_symbol, pe_price = get_cheapest_option_price("PE", PEX_Strike, kite, index_type='NIFTY')

    print(f"BCE Strike: {BCEX_Strike}, Cheapest BCE: Symbol={bce_symbol}, Price={bce_price}")
    print(f"CE Strike: {CEX_Strike}, Cheapest CE: Symbol={ce_symbol}, Price={ce_price}")
    print(f"PE Strike: {PEX_Strike}, Cheapest PE: Symbol={pe_symbol}, Price={pe_price}")
    print(f"BPE Strike: {BPEX_Strike}, Cheapest BPE: Symbol={bpe_symbol}, Price={bpe_price}")

    # Checking if the strikes are available at a cheaper price
    if bce_price == BCEX_Strike:
        print(f"The BCE strike is not available at a cheaper price: {bce_symbol} at {bce_price}")
    if ce_price == CEX_Strike:
        print(f"The CE strike is not available at a cheaper price: {ce_symbol} at {ce_price}")
    if pe_price == PEX_Strike:
        print(f"The PE strike is not available at a cheaper price: {pe_symbol} at {pe_price}")
    if bpe_price == BPEX_Strike:
        print(f"The BPE strike is not available at a cheaper price: {bpe_symbol} at {bpe_price}")

if __name__ == "__main__":
    try:
        kite = get_kite()
        print_cheapest_prices(kite)

        BCE_Strike, CE_Strike, PE_Strike, BPE_Strike = get_prices()
        print(f"BCE Strike Price: {BCE_Strike}")
        print(f"CE Strike Price: {CE_Strike}")
        print(f"PE Strike Price: {PE_Strike}")
        print(f"BPE Strike Price: {BPE_Strike}")
    except Exception as e:
        remove_token(dir_path)
        logging.error(f"{str(e)} unable to get holdings")
        sys.exit(1)


