import yfinance as yf
import pandas as pd
import warnings
from rich.console import Console
from colorama import Fore, Style, init

init(autoreset=True)  # Initialize Colorama

console = Console()
warnings.simplefilter(action='ignore', category=FutureWarning)

OHLC_COLUMNS = ['Open', 'High', 'Low', 'Close']

def get_nifty50_data(period="5d"):
    ticker_symbol = "^NSEI"  # NIFTY50 index symbol on Yahoo Finance
    try:
        nifty_data = yf.Ticker(ticker_symbol).history(period=period)
        ohlc_data = nifty_data[OHLC_COLUMNS]
        return ohlc_data
    except Exception as e:
        print(f"Error fetching data: {e}")
        return pd.DataFrame()

def get_previous_day_close(df):
    if len(df) >= 2:
        return df.iloc[-2]['Close']
    else:
        return None

def get_today_close():
    nifty50_ohlc = get_nifty50_data(period="1d")
    if not nifty50_ohlc.empty:
        prev_close = get_previous_day_close(nifty50_ohlc)
        return nifty50_ohlc.iloc[-1]['Close'], prev_close
    else:
        return None, None

def dayprinter(o, h, l, c, prev_close):
    max_total_length = 42
    try:
        candle_length = h - l
        if c > o:
            n = round(((o - l) / candle_length) * 100)
            x = round(((c - o) / candle_length) * 100)
            m = 100 - n - x
        else:
            n = round(((c - l) / candle_length) * 100)
            x = round(((o - c) / candle_length) * 100)
            m = 100 - n - x
        
        n_length = round((n / 100) * max_total_length)
        x_length = round((x / 100) * max_total_length)
        m_length = max_total_length - n_length - x_length
        
        print(Fore.LIGHTBLACK_EX + '█' * n_length, end='')
        if c > o:
            print(Fore.GREEN + '█' * x_length + Style.RESET_ALL, end='')
        elif o > c:
            print(Fore.RED + '█' * x_length + Style.RESET_ALL, end='')
        print(Fore.LIGHTBLACK_EX + '█' * m_length)
    
    except Exception as e:
        pass

def fetch_data(symbol):
    data = yf.Ticker(symbol).history(period="5d", interval="1m")
    return data

def calculate_heikin_ashi_colors(data):
    ha_close = (data['Open'] + data['High'] + data['Low'] + data['Close']) / 4
    ha_open = ha_close.shift(1)
    colors = ['🟥' if ha_close.iloc[-i] < ha_open.iloc[-i] else '🟩' for i in range(1, min(4, len(ha_close) + 1))][::-1]

    current_color = 'Bear' if ha_close.iloc[-1] < ha_open.iloc[-1] else 'Bull'
    last_closed_color = 'Bear' if ha_close.iloc[-2] < ha_open.iloc[-2] else 'Bull'

    candle_sequence = f'{"".join(colors)}'
    return candle_sequence, current_color, last_closed_color

def calculate_last_twenty_heikin_ashi_colors(symbol):
    current_utc_time = time.gmtime().tm_hour * 60 + time.gmtime().tm_min

    if START_TIME <= current_utc_time < END_TIME:
        data = yf.Ticker(symbol).history(period="5d", interval="5m")
    else:
        data = fetch_data(symbol)

    return calculate_heikin_ashi_colors(data)

def get_market_check(symbol):
    candle_sequence, current_color, last_closed_color = calculate_last_twenty_heikin_ashi_colors(symbol)

    if current_color == 'Bear' and last_closed_color == 'Bear':
        market_signal = 'Bear'
    elif current_color == 'Bull' and last_closed_color == 'Bull':
        market_signal = 'Bull'
    elif current_color == 'Bear' and last_closed_color == 'Bull':
        market_signal = 'Sell'
    elif current_color == 'Bull' and last_closed_color == 'Bear':
        market_signal = 'Buy'
    else:
        market_signal = 'None'

    return candle_sequence, market_signal

def get_stock_action(ticker):
    ha_action = None
    stock_power = 0.0
    day_change = 0.0
    open_change = 0.0

    try:
        data = yf.Ticker(ticker).history(period="5d")
        today_open = data['Open'].iloc[-1]
        today_high = data['High'].iloc[-1]
        today_low = data['Low'].iloc[-1]
        current_price = data['Close'].iloc[-1]
        today_average = (today_open + today_high + today_low + current_price) / 4
        
        yesterday_close = data['Close'].iloc[-2]
        yesterday_open = data['Open'].iloc[-2]
        yesterday_average = (yesterday_close + yesterday_open + today_open) / 3
        
        raw_stock_power = (current_price - (today_low - 0.01)) / (abs(today_high + 0.01) - abs(today_low - 0.01))
        stock_power = round(max(0.1, min(raw_stock_power, 1.0)), 2)
        day_change = round(((current_price - yesterday_close) / yesterday_close) * 100, 2)
        open_change = round(((current_price - today_open) / today_open) * 100, 2)

        ha_close = (data['Open'] + data['High'] + data['Low'] + data['Close']) / 4
        ha_open = ha_close.shift(1)
        
        ha_action = "Bullish" if ha_close.iloc[-1] > ha_open.iloc[-1] else "Bearish"

    except Exception as e:
        pass

    return ha_action, stock_power, day_change, open_change

def calculate_consecutive_candles(tickerSymbol):
    warnings.filterwarnings("ignore")

    try:
        tickerData = yf.Ticker(tickerSymbol)
        tickerDf = tickerData.history(period='5d', interval='1m')

        ha_close = (tickerDf['Open'] + tickerDf['High'] + tickerDf['Low'] + tickerDf['Close']) / 4
        ha_open = ha_close.shift(1)
        ha_color = pd.Series('green', index=ha_close.index)
        ha_color[ha_close < ha_open] = 'red'

        consecutive_count = 1
        current_color = None

        for i in range(1, len(ha_color)):
            if ha_color[i] == ha_color[i - 1]:
                consecutive_count += 1
            else:
                consecutive_count = 1
                current_color = ha_color[i]

        if current_color is not None:
            if consecutive_count > 9:
                consecutive_count = 9
            if current_color == 'green':
                cedepth = consecutive_count
                pedepth = 1
            else:
                cedepth = 1
                pedepth = consecutive_count
            return cedepth, pedepth
    except Exception as e:
        return f"An error occurred: {e}"

# Call the function with the ticker as an argument
ticker_symbol = '^NSEI'  # You can change this to any valid ticker symbol
ha_action, stock_power, day_change, open_change = get_stock_action(ticker_symbol)

# Print the results for stock action
print(f"Ticker: {ticker_symbol}")
print(f"Heikin-Ashi Action: {ha_action}")
print(f"Stock Power: {stock_power}")
print(f"Day Change (%): {day_change}")
print(f"Open Change (%): {open_change}")

# Call the market check function and print the candle sequence and market signal
candle_sequence, market_signal = get_market_check(ticker_symbol)
print(f"Candle Sequence: {candle_sequence}")
print(f"Market Signal: {market_signal}")

# Example usage of calculate_consecutive_candles
cedepth, pedepth = calculate_consecutive_candles(ticker_symbol)
print(f"Consecutive Candle Depths: Cedepth = {cedepth}, Pedepth = {pedepth}")
