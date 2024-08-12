from rich import print
import sys
import yfinance as yf
import warnings

# Set the python3IOENCODING environment variable to 'utf-8'
sys.stdout.reconfigure(encoding='utf-8')

# Suppress yfinance warnings
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)

def get_nse_action():
    ha_nse_action = None
    nse_power = 0.0
    Day_Change = 0.0
    Open_Change = 0.0
    try:
        # Download data for a fixed 5-day period
        data = yf.Ticker('^NSEI').history(period="5d")

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

        ha_close = (data['Open'] + data['High'] + data['Low'] + data['Close']) / 4
        ha_open = (data['Open'].shift(1) + data['Close'].shift(1)) / 2
        ha_high = data[['High', 'Open', 'Close']].max(axis=1)
        ha_low = data[['Low', 'Open', 'Close']].min(axis=1)
        
        # Define Heikin-Ashi day candle status
        ha_nse_action = "Bullish" if ha_close.iloc[-1] > ha_open.iloc[-1] else "Bearish"

    except Exception as e:
        # print(f"Error during data download for 5 days: {e}")
        pass  # Ignore print statement

    return ha_nse_action, nse_power, Day_Change, Open_Change  # Return calculated values

ha_nse_action, nse_power, Day_Change, Open_Change = get_nse_action()
