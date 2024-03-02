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

def get_bnk_action():
    try:
        # Download data for a fixed 5-day period
        data = yf.Ticker('^NSEBANK').history(period="7d")

        # Extract today's open, yesterday's close, and current price
        today_open = data['Open'].iloc[-1]
        today_high = data['High'].iloc[-1]
        today_low = data['Low'].iloc[-1]
        current_price = data['Close'].iloc[-1]

        today = (today_open + today_high + today_low + current_price) / 4
        
        yesterday_close = data['Close'].iloc[-2]
        yesterday_open = data['Open'].iloc[-2]

        yesterday = (yesterday_close + yesterday_open + today_open) / 3
        
        # Calculate bnk_power
        raw_bnk_power = (current_price - (today_low - 0.01)) / (abs(today_high + 0.01) - abs(today_low - 0.01))
        bnk_power = round(max(0.1, min(raw_bnk_power, 1.0)), 2)
        Day_bnk_Change = round(((current_price - yesterday_close) / yesterday_close) * 100, 2)
        Open_bnk_Change = round(((current_price - today_open) / today_open) * 100, 2)
        OPTIONS = round(current_price / 50) * 50 if current_price % 100 < 50 else round(current_price / 100) * 100

        # Determine if today's candle is bullish or bearish compared to yesterday
        # Initialize Day Action as an empty string
        bnk_action = ""
        if today > yesterday:
            bnk_action = "Bullish"
            OPTIONS = round(current_price / 50) * 50 if current_price % 100 < 50 else round(current_price / 100) * 100
        elif today < yesterday:
            bnk_action = "Bearish"
            OPTIONS = round(current_price / 50) * 50 if current_price % 100 < 50 else round(current_price / 100) * 100
        else:
            return 'Neutral', bnk_power, Day_bnk_Change, Open_bnk_Change, OPTIONS  # Return neutral along with other values

    except Exception as e:
        print(f"Error during data download for 5 days: {e}")

    return bnk_action, bnk_power, Day_bnk_Change, Open_bnk_Change, OPTIONS  # Return calculated values

# Call the get_bnk_action function
bnk_action, bnk_power, Day_bnk_Change, Open_bnk_Change, OPTIONS = get_bnk_action()
#print("bnk Action:", bnk_action, "\nbnk Power:", bnk_power, "\nDay Change:", Day_bnk_Change, "\nOpen Change:", Open_bnk_Change, "\nOPTIONS:", OPTIONS)
