import yfinance as yf
import os
import sys

# Define the stock symbol (NSEI for Nifty 50)

def analyze_stock(symbol):
    try:
        # Redirect standard output to os.devnull to suppress messages
        sys.stdout = open(os.devnull, 'w')

        # Download today's data
        data = yf.download(symbol, period="7d")
    except Exception as e:
        print(f"Error during data download: {e}")
        return "Error", None
    finally:
        # Restore standard output
        sys.stdout.close()
        sys.stdout = sys.__stdout__

    # Extract today's open, yesterday's close, and current price
    today_open = data['Open'].iloc[-1]
    today_high = data['High'].iloc[-1]
    today_low = data['Low'].iloc[-1]
    yesterday_close = data['Close'].iloc[-2]
    current_price = data['Close'].iloc[-1]

    # Check if the conditions are met
    below_open_high_above_open = (today_low < today_open) & (today_high > today_open)
    above_open_low_below_open = (today_high > today_open) & (today_low < today_open)

    if below_open_high_above_open.any() or above_open_low_below_open.any():
        return 'yes'
    else:
        return 'no'





