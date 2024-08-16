import yfinance as yf
import logging
import random
from fundpxy import calculate_decision

decision, optdecision, available_cash, live_balance, limit = calculate_decision()

# Initialize logger
logging.basicConfig(level=logging.WARNING) 
logger = logging.getLogger(__name__)

def calculate_heikin_ashi_colors(data):
    if data.empty:
        logger.warning("Data is empty. Cannot calculate Heikin-Ashi colors.")
        return None, None, None

    logger.debug(f"Calculating Heikin-Ashi colors for data:\n{data.head()}")
    ha_close = (data['Open'] + data['High'] + data['Low'] + data['Close']) / 4
    ha_open = (data['Open'].shift(1) + data['Close'].shift(1)) / 2

    current_color = 'Bear' if ha_close.iloc[-1] < ha_open.iloc[-1] else 'Bull'
    last_closed_color = 'Bear' if ha_close.iloc[-2] < ha_open.iloc[-2] else 'Bull'
    last_last_closed_color = 'Bear' if ha_close.iloc[-3] < ha_open.iloc[-3] else 'Bull'
    
    logger.debug(f"Heikin-Ashi colors: current={current_color}, last_closed={last_closed_color}, last_last_closed={last_last_closed_color}")
    return current_color, last_closed_color, last_last_closed_color

def calculate_macd(data):
    if data.empty:
        logger.warning("Data is empty. Cannot calculate MACD.")
        return None, None

    logger.debug(f"Calculating MACD for data:\n{data.head()}")
    short_ema = data['Close'].ewm(span=12, adjust=False).mean()
    long_ema = data['Close'].ewm(span=26, adjust=False).mean()
    macd = short_ema - long_ema
    signal = macd.ewm(span=9, adjust=False).mean()
    logger.debug(f"MACD calculated:\n{macd.tail()}, Signal:\n{signal.tail()}")
    return macd, signal

def check_ha_candles(symbol):
    logger.debug(f"Checking Heikin-Ashi candles for symbol: {symbol}")
    data = yf.Ticker(symbol).history(period="3mo", interval="1d")

    if data.empty:
        logger.error(f"No data found for symbol: {symbol}")
        return "No Data"

    current_data = data.tail(5)
    
    current_color, last_closed_color, last_last_closed_color = calculate_heikin_ashi_colors(current_data)

    if current_color is None or last_closed_color is None or last_last_closed_color is None:
        return "No Data"

    data['50d_SMA'] = data['Close'].rolling(window=50).mean()
    current_price = data['Close'].iloc[-1]
    sma_50 = data['50d_SMA'].iloc[-1]
    above_50d_sma = current_price > sma_50
    
    macd, signal = calculate_macd(data)
    if macd is None or signal is None:
        return "No Data"

    macd_above_0 = macd.iloc[-1] > 0

    if (last_closed_color == 'Bear' and 
        last_last_closed_color == 'Bear' and 
        current_color == 'Bull' and 
        above_50d_sma and 
        macd_above_0):
        smbpxy = 'Buy'
    else:
        smbpxy = 'Hold'

    logger.debug(f"Heikin-Ashi decision for {symbol}: {smbpxy}")
    return smbpxy

from ordcncpxy import place_buy_order

# Read symbols from file, shuffle them, and append suffix
def read_symbols_from_file(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
    # Skip header and append suffix to each symbol
    symbols = [line.strip() + '.NS' for line in lines[1:] if line.strip()]
    random.shuffle(symbols)  # Shuffle the list of symbols
    return symbols

# Main function to check and print smbpxy and place orders
def main():
    if live_balance > limit:
        filename = 'avgstocks'  # File containing the list of stock symbols (no extension)
        avgstocks = read_symbols_from_file(filename)
        
        for symbol in avgstocks:
            smbpxy = check_ha_candles(symbol)
            print(f"{symbol}: {smbpxy}")
            if smbpxy == 'Buy':
                kite_symbol = symbol.replace('.NS', '')
                place_buy_order(kite_symbol)
    else:
        print(f"Cash:{live_balance}.Limit:{limit}.No buy.")
if __name__ == "__main__":
    main()
