from rich import print
from colorama import Fore, Style
import sys
import yfinance as yf
import time
import warnings
from macdpxy import calculate_macd_signal
from smapxy import check_index_status

# Suppress yfinance warnings
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)

def get_nse_action():
    try:
        # Download data for a fixed 5-day period
        data = yf.Ticker('^NSEI').history(period="7d")

        # Extract today's open, yesterday's close, and current price
        today_open = data['Open'].iloc[-1]
        today_high = data['High'].iloc[-1]
        today_low = data['Low'].iloc[-1]
        current_price = data['Close'].iloc[-1]

        today = (today_open + today_high + today_low + current_price) / 4
        
        yesterday_close = data['Close'].iloc[-2]
        yesterday_open = data['Open'].iloc[-2]

        yesterday = (yesterday_close + yesterday_open + today_open) / 3
        
        # Calculate nse_power
        raw_nse_power = (current_price - (today_low - 0.01)) / (abs(today_high + 0.01) - abs(today_low - 0.01))
        nse_power = round(max(0.1, min(raw_nse_power, 1.0)), 2)
        Day_Change = round(((current_price - yesterday_close) / yesterday_close) * 100, 2)
        Open_Change = round(((current_price - today_open) / today_open) * 100, 2)
        OPTIONS = round(current_price / 50) * 50 if current_price % 100 < 50 else round(current_price / 100) * 100

        # Determine if today's candle is bullish or bearish compared to yesterday
        # Initialize Day Action as an empty string
        nse_action = ""
        if today > yesterday:
            nse_action = "Bullish"
            OPTIONS = round(current_price / 50) * 50 if current_price % 100 < 50 else round(current_price / 100) * 100
        elif today < yesterday:
            nse_action = "Bearish"
            OPTIONS = round(current_price / 50) * 50 if current_price % 100 < 50 else round(current_price / 100) * 100
        else:
            return 'Neutral', nse_power, Day_Change, Open_Change, OPTIONS  # Return neutral along with other values

    except Exception as e:
        print(f"Error during data download for 5 days: {e}")

    return nse_action, nse_power, Day_Change, Open_Change, OPTIONS  # Return calculated values

# Set the python3IOENCODING environment variable to 'utf-8'
sys.stdout.reconfigure(encoding='utf-8')

# Call the get_nse_action function
nse_action, nse_power, Day_Change, Open_Change, OPTIONS = get_nse_action()

day_change_sign = '+' if Day_Change > 0 else ''
open_change_sign = '+' if Open_Change > 0 else ''

# Print the formatted output using rich print
print(f"🔆{day_change_sign}{Fore.GREEN if Day_Change >= 0 else Fore.RED}{Day_Change:.2f}{Style.RESET_ALL}⌛{open_change_sign}{Fore.GREEN if Open_Change >= 0 else Fore.RED}{Open_Change:.2f}{Style.RESET_ALL}⚡{Fore.GREEN if nse_power > 0.5 else Fore.RED}{nse_power:.2f}{Style.RESET_ALL}🟥-{pedepth}🚦📈-{close_color}{int(today_close[0])}{macd}🚦{cedepth}+🟩")

