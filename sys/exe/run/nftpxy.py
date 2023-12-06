import yfinance as yf
import os
import sys

def get_nse_action():
    # Define the stock symbol (NSEI for Nifty 50)
    stock_symbol = "^NSEI"

    for days in range(1, 8):
        try:
            # Redirect standard output to os.devnull to suppress messages
            sys.stdout = open(os.devnull, 'w')

            # Download data for the specified number of days
            data = yf.download(stock_symbol, period=f"{days}d")

            # Extract today's open, yesterday's close, and current price
            today_open = data['Open'].iloc[-1]
            today_high = data['High'].iloc[-1]
            today_low = data['Low'].iloc[-1]
            current_price = data['Close'].iloc[-1]
            
            yesterday_close = data['Close'].iloc[-2]
            yesterday_open = data['Open'].iloc[-2]
            
            # Calculate nse_power
            nse_power = round((current_price - (today_low - 0.01)) / (abs(today_high + 0.01) - abs(today_low - 0.01)), 2)

            # Initialize Day Action as an empty string
            nse_action = ""

            # Determine the candlestick condition for today
            if yesterday_close > yesterday_open and current_price > today_open and current_price > yesterday_close:
                nse_action = "SuperBull"
            elif yesterday_close > yesterday_open and current_price < today_open and current_price < yesterday_close:
                nse_action = "SuperBear"
            elif yesterday_close < yesterday_open and current_price > today_open and current_price > yesterday_close:
                nse_action = "DangerBull"
            elif yesterday_close < yesterday_open and current_price < today_open and current_price < yesterday_close:
                nse_action = "DangerBear"
            elif current_price < today_open:
                nse_action = "Bear"
            elif current_price > today_open:
                nse_action = "Bull"
            else:
                
                nse_action = "Neutral"

            return nse_action, nse_power

        except Exception as e:
            print(f"Error during data download for {days} days: {e}")
        finally:
            # Restore standard output
            sys.stdout.close()
            sys.stdout = sys.__stdout__

    return "Error", None

# Call the get_nse_action function
nse_action, nse_power = get_nse_action()
# ANSI escape code for bright yellow color
yellow_color_code = "\033[93m"
reset_color_code = "\033[0m"

# Print the text in bright yellow
print(f"{yellow_color_code}Market is {nse_action}⚡💥<====>power⚡💥{nse_power}{reset_color_code}💥⚡")


