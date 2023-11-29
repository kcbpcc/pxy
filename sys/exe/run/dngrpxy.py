import yfinance as yf
import os
import sys

def dangerbear(symbol):
    for days in range(2, 8):
        try:
            # Redirect standard output to os.devnull to suppress messages
            sys.stdout = open(os.devnull, 'w')

            # Download data for the specified number of days
            data = yf.download(symbol, period=f"{days}d")

            # Extract relevant values
            yesterday_open = data['Open'].iloc[-2]
            today_open = data['Open'].iloc[-1]
            yesterday_close = data['Close'].iloc[-2]
            current_price = data['Close'].iloc[-1]

            # Check if the conditions are met
            danger_bear = (yesterday_close < yesterday_open) and (current_price < today_open) and (current_price < yesterday_close)

            if danger_bear:
                return 'YES'

        except Exception as e:
            print(f"Error during data download for {days} days: {e}")
        finally:
            # Restore standard output
            sys.stdout.close()
            sys.stdout = sys.__stdout__

    return 'NO'

# The function now returns 'YES' if the danger bear condition is met for any of the days in the range, and 'NO' otherwise.
