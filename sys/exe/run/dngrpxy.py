import yfinance as yf
import os
import sys

# Define the stock symbol (NSEI for Nifty 50)

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
        #sys.stdout = sys.__stdout__

    # Extract today's open, yesterday's close, and current price
    yesterday_open = today_open = data['Open'].iloc[-2]
    today_open = data['Open'].iloc[-1]
    today_high = data['High'].iloc[-1]
    today_low = data['Low'].iloc[-1]
    yesterday_close = data['Close'].iloc[-2]
    current_price = data['Close'].iloc[-1]

    # Check if the conditions are met
    dangerbear = (yesterday_close < yesterday_open) & (current_price < today_open) & (current_price < yesterday_close) 
  

    if DangerBear.any() :
        return 'yes'
    else:
        return 'no'
