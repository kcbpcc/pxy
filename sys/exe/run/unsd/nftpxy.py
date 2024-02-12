from rich import print
import sys
import yfinance as yf
import time
import warnings

# Set the python3IOENCODING environment variable to 'utf-8'
sys.stdout.reconfigure(encoding='utf-8')

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
        
        yesterday_close = data['Close'].iloc[-2]
        yesterday_open = data['Open'].iloc[-2]
        
        # Calculate nse_power
        raw_nse_power = (current_price - (today_low - 0.01)) / (abs(today_high + 0.01) - abs(today_low - 0.01))
        nse_power = round(max(0.1, min(raw_nse_power, 1.0)), 2)
        Day_Change = round(((current_price - yesterday_close) / yesterday_close) * 100, 2)
        Open_Change = round(((current_price - today_open) / today_open) * 100, 2)
        OPTIONS = round(current_price / 50) * 50 if current_price % 100 < 50 else round(current_price / 100) * 100

        # Initialize Day Action as an empty string
        nse_action = ""

        # Determine the candlestick condition for today
        if yesterday_close < current_price and today_open < current_price:
            nse_action = "Bullish"
            OPTIONS = round(current_price / 50) * 50 if current_price % 100 < 50 else round(current_price / 100) * 100
        elif yesterday_close > current_price and today_open > current_price:
            nse_action = "Bearish"
            OPTIONS = round(current_price / 50) * 50 if current_price % 100 < 50 else round(current_price / 100) * 100
        elif today_open < current_price:
            nse_action = "Bull"  
            OPTIONS = round(current_price / 50) * 50 if current_price % 100 < 50 else round(current_price / 100) * 100
        elif today_open > current_price:
            nse_action = "Bear" 
            OPTIONS = round(current_price / 50) * 50 if current_price % 100 < 50 else round(current_price / 100) * 100
        else:
            nse_action = "Bull"
            OPTIONS = round(current_price / 50) * 50 if current_price % 100 < 50 else round(current_price / 100) * 100
        return nse_action, nse_power, Day_Change, Open_Change, OPTIONS 

    except Exception as e:
        print(f"Error during data download for 5 days: {e}")

    return "Error", None

# Call the get_nse_action function
nse_action, nse_power, Day_Change, Open_Change, OPTIONS = get_nse_action()



