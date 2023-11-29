import yfinance as yf
import os
import sys

def dangerbear(symbol):
    try:
        # Redirect standard output to os.devnull to suppress messages
        sys.stdout = open(os.devnull, 'w')

        # Download today's data
        data = yf.download(symbol, period="5d")
    except Exception as e:
        print(f"Error during data download: {e}")
        return "Error", None
    finally:
        # Restore standard output
        sys.stdout.close()
        sys.stdout = sys.__stdout__

    # Extract relevant values
    yesterday_open = data['Open'].iloc[-2]
    today_open = data['Open'].iloc[-1]
    yesterday_close = data['Close'].iloc[-2]
    current_price = data['Close'].iloc[-1]

    # Check if the conditions are met
    danger_bear = (yesterday_close < yesterday_open) and (current_price < today_open) and (current_price < yesterday_close)

    if danger_bear:
        return 'YES'
    else:
        return 'NO'
