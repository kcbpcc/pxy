import yfinance as yf
import logging
from datetime import datetime
from login_get_kite import get_kite, remove_token
from cnstpxy import dir_path

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
    BCE_Strike = round_to_nearest_100(get_current_price('^NSEBANK'))
    CE_Strike = round_to_nearest_100(get_current_price('^NSEI'))
    PE_Strike = round_to_nearest_100(get_current_price('^NSEI'))
    BPE_Strike = round_to_nearest_100(get_current_price('^NSEBANK'))
    return BCE_Strike, CE_Strike, PE_Strike, BPE_Strike

def get_cheapest_option_price(option_type, strike_price, kite):
    strikes = [strike_price, strike_price + 100, strike_price - 100]
    cheapest_price = float('inf')
    cheapest_symbol = None

    for strike in strikes:
        if option_type in ["CE", "PE"]:
            symbol = f"NIFTY24AUG{strike:05d}{option_type}"
        else:
            symbol = f"BANKNIFTY24AUG{strike:05d}{option_type}"
        
        try:
            logging.info(f"Checking symbol: NFO:{symbol}")
            response = kite.ltp(f"NFO:{symbol}")
            ltp = response[f"NFO:{symbol}"]["last_price"]
            if ltp < cheapest_price:
                cheapest_price = ltp
                cheapest_symbol = symbol
        except Exception as e:
            logging.error(f"Error fetching price for {symbol}: {e}")

    return cheapest_symbol, cheapest_price

def print_cheapest_prices(kite):
    BCE_Strike, CE_Strike, PE_Strike, BPE_Strike = get_strikes()

    # For BankNifty options
    bce_symbol, bce_price = get_cheapest_option_price("CE", BCE_Strike, kite)
    bpe_symbol, bpe_price = get_cheapest_option_price("PE", BPE_Strike, kite)

    # For Nifty options
    ce_symbol, ce_price = get_cheapest_option_price("CE", CE_Strike, kite)
    pe_symbol, pe_price = get_cheapest_option_price("PE", PE_Strike, kite)

    print(f"BCE Strike: {BCE_Strike}, Cheapest BCE: Symbol={bce_symbol}, Price={bce_price}")
    print(f"CE Strike: {CE_Strike}, Cheapest CE: Symbol={ce_symbol}, Price={ce_price}")
    print(f"PE Strike: {PE_Strike}, Cheapest PE: Symbol={pe_symbol}, Price={pe_price}")
    print(f"BPE Strike: {BPE_Strike}, Cheapest BPE: Symbol={bpe_symbol}, Price={bpe_price}")

    # Checking if the strikes are available at a cheaper price
    if bce_price == BCE_Strike:
        print(f"The BCE strike is not available at a cheaper price: {bce_symbol} at {bce_price}")
    if ce_price == CE_Strike:
        print(f"The CE strike is not available at a cheaper price: {ce_symbol} at {ce_price}")
    if pe_price == PE_Strike:
        print(f"The PE strike is not available at a cheaper price: {pe_symbol} at {pe_price}")
    if bpe_price == BPE_Strike:
        print(f"The BPE strike is not available at a cheaper price: {bpe_symbol} at {bpe_price}")

if __name__ == "__main__":
    try:
        kite = get_kite()
        print_cheapest_prices(kite)
    except Exception as e:
        remove_token(dir_path)
        logging.error(f"{str(e)} unable to get holdings")
        sys.exit(1)


