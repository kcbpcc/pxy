import warnings
import yfinance as yf
import pandas as pd
from rich.console import Console
from colorama import Fore, Style, init
from mktpxy import get_market_check
from utcpxy import peak_time
from macdpxy import calculate_macd_signal
from smapxy import check_index_status
from depthpxy import calculate_consecutive_candles

# Initialize Colorama and Rich Console
init(autoreset=True)
console = Console()

# Suppress specific warnings
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)

OHLC_COLUMNS = ['Open', 'High', 'Low', 'Close']

def get_nifty50_data(period="5d"):
    ticker_symbol = "^NSEI"  # NIFTY50 index symbol on Yahoo Finance
    try:
        nifty_data = yf.Ticker(ticker_symbol).history(period=period)
        ohlc_data = nifty_data[OHLC_COLUMNS]
        return ohlc_data
    except Exception as e:
        console.print(f"[bold red]Error fetching data:[/bold red] {e}")
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
        console.print(f"[bold red]Error in dayprinter:[/bold red] {e}")

def fetch_data(symbol):
    data = yf.Ticker(symbol).history(period="5d", interval="1m")
    return data

def calculate_heikin_ashi_colors(data):
    ha_close = (data['Open'] + data['High'] + data['Low'] + data['Close']) / 4
    ha_open = (data['Open'].shift(1) + data['Close'].shift(1)) / 2

    colors = ['🟥' if ha_close.iloc[-i] < ha_open.iloc[-i] else '🟩' for i in range(1, min(4, len(ha_close) + 1))][::-1]

    current_color = 'Bear' if ha_close.iloc[-1] < ha_open.iloc[-1] else 'Bull'
    last_closed_color = 'Bear' if ha_close.iloc[-2] < ha_open.iloc[-2] else 'Bull'

    candle_sequence = f'{"".join(colors)}'
    return candle_sequence, current_color, last_closed_color

def get_stock_action(ticker):
    ha_action, stock_power, day_change, open_change = None, 0.0, 0.0, 0.0
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
        ha_open = (data['Open'].shift(1) + data['Close'].shift(1)) / 2

        ha_action = "Bullish" if ha_close.iloc[-1] > ha_open.iloc[-1] else "Bearish"

    except Exception as e:
        console.print(f"[bold red]Error in get_stock_action:[/bold red] {e}")

    return ha_action, stock_power, day_change, open_change

def main():
    ticker_symbol = '^NSEI'
    ha_action, stock_power, day_change, open_change = get_stock_action(ticker_symbol)
    
    console.print(f"Ticker: {ticker_symbol}")
    console.print(f"Heikin-Ashi Action: {ha_action}")
    console.print(f"Stock Power: {stock_power}")
    console.print(f"Day Change (%): {day_change}")
    console.print(f"Open Change (%): {open_change}")

    candle_sequence, market_signal = get_market_check(ticker_symbol)
    console.print(f"Candle Sequence: {candle_sequence}")
    console.print(f"Market Signal: {market_signal}")

    cedepth, pedepth = calculate_consecutive_candles(ticker_symbol)
    console.print(f"CEDepth: {cedepth}")
    console.print(f"PEDepth: {pedepth}")

if __name__ == "__main__":
    main()

