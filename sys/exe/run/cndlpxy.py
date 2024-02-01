import warnings
import yfinance as yf
import pandas as pd
import colorama
from colorama import Fore, Style  # Add Style to the imports

colorama.init(autoreset=True)

OHLC_COLUMNS = ['Open', 'High', 'Low', 'Close']

def get_nifty50_data(days=2):
    ticker_symbol = "^NSEI"  # NIFTY50 index symbol on Yahoo Finance

    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=FutureWarning)
            # Create a Ticker object
            nifty_ticker = yf.Ticker(ticker_symbol)

            # Get historical data for specified number of days
            nifty_data = nifty_ticker.history(period=f'{days}d')

        # Extract OHLC data
        ohlc_data = nifty_data[OHLC_COLUMNS]

        return ohlc_data

    except Exception as e:
        print(f"Error fetching data: {e}")
        return pd.DataFrame()  # Return an empty DataFrame in case of an error

def get_previous_day_close():
    nifty50_ohlc = get_nifty50_data(days=2)
    if not nifty50_ohlc.empty:
        return nifty50_ohlc.iloc[-2]['Close']
    else:
        return None  # Handle the case when data is not available

def get_today_close():
    nifty50_ohlc = get_nifty50_data(days=1)
    if not nifty50_ohlc.empty:
        return nifty50_ohlc.iloc[-1]['Close']
    else:
        return None  # Handle the case when data is not available

def dayprinter(o, h, l, c, prev_close):
    total_length = 20
    
    # Calculate the lengths of different segments as percentages
    if c > o:
        n = round(((o - (l-1)) / ((h+1) - (l-1))) * 100)
        x = round(((c - o) / ((h+1) - (l-1))) * 100)
        m = 100 - n - x
    else:
        n = round(((c - (l-1)) / ((h+1) - (l-1))) * 100)
        x = round(((o - c) / ((h+1) - (l-1))) * 100)
        m = 100 - n - x

    # Print both the previous day's close and today's close in a single sentence with color
    arrow = "━━🟢🟢━━" if c > prev_close else "━━🔴🔴━━"
    total_width = 43
    first_line = f"{int(prev_close)}{arrow}{int(c)}"
    second_line = Fore.LIGHTWHITE_EX + '━' * int((n / 100) * total_length)
    
    if c > o:
        second_line += Fore.GREEN + '▌' * int((x / 100) * total_length) + Style.RESET_ALL
    elif o > c:
        second_line += Fore.RED + '▌' * int((x / 100) * total_length) + Style.RESET_ALL
    
    second_line += Fore.LIGHTWHITE_EX + '━' * int((m / 100) * total_length)
    
    # Calculate the space available for the second line
    available_space = total_width - len(first_line)
    # Combine both lines with appropriate spacing
    output = f"{first_line:<{available_space}}{second_line}"
    
    print(output)
    # Determine the color based on the comparison of today's close with yesterday's close
    color = Fore.GREEN if c > prev_close else Fore.RED
    
def option_to_trade():
    today_data = get_nifty50_data().iloc[-1][OHLC_COLUMNS]
    today_open = today_data['Open']
    today_close = today_data['Close']
    option_value = round(today_close / 50) * 50
    return option_value

# Example usage in the main program
previous_day_close = get_previous_day_close()
today_close = get_today_close()

if previous_day_close is not None and today_close is not None:
    today_data = get_nifty50_data().iloc[-1][OHLC_COLUMNS]
    dayprinter(*today_data, previous_day_close)
else:
    print("Unable to fetch data.")
