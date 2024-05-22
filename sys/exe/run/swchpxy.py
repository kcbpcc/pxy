# PXY®
import yfinance as yf
import os
import sys

def analyze_stock():
    try:
        # Redirect standard output to os.devnull to suppress messages
        sys.stdout = open(os.devnull, 'w')

        # Download data for the specified 2-day period
        data = yf.Ticker('^NSEI').history(period="5d")

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
    except Exception as e:
        print(f"Error during data download for 2 days: {e}")
    finally:
        # Restore standard output
        sys.stdout.close()
        sys.stdout = sys.__stdout__

    return 'no'










