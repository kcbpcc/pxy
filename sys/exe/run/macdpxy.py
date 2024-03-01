import yfinance as yf
import pandas as pd

def calculate_macd_signal(ticker_symbol):
    # Create a Ticker object
    nifty_ticker = yf.Ticker(ticker_symbol)

    # Fetch one-minute intraday data for the current day
    data = nifty_ticker.history(period='5d', interval='2m')

    # Calculate MACD
    short_window = 12
    long_window = 26

    # Calculate short-term exponential moving average
    short_ema = data['Close'].ewm(span=short_window, min_periods=1, adjust=False).mean()

    # Calculate long-term exponential moving average
    long_ema = data['Close'].ewm(span=long_window, min_periods=1, adjust=False).mean()

    # Calculate MACD line
    macd_line = short_ema - long_ema

    # Calculate signal line
    signal_line = macd_line.ewm(span=9, min_periods=1, adjust=False).mean()

    # Calculate MACD histogram
    macd_histogram = macd_line - signal_line

    # Determine if MACD crossed above or below signal line
    current_macd_histogram = macd_histogram.iloc[-1]
    previous_macd_histogram = macd_histogram.iloc[-2]
    current_macd_line = macd_line.iloc[-1]

    if previous_macd_histogram < 0 and current_macd_histogram > 0:
        # Scenario 1: Previous MACD histogram was negative, and current MACD histogram is positive
        macd_signal = "👆"  # MACD histogram is rising
    
    elif previous_macd_histogram > 0 and current_macd_histogram < 0:
        # Scenario 2: Previous MACD histogram was positive, and current MACD histogram is negative
        macd_signal = "👇"  # MACD histogram is falling
    
    elif previous_macd_histogram > 0 and current_macd_histogram > 0:
        # Scenario 3: Previous MACD histogram was positive, and current MACD histogram is also positive
        macd_signal = "👉"  # MACD histogram is steady or increasing
    
    elif previous_macd_histogram < 0 and current_macd_histogram < 0:
        # Scenario 4: Previous MACD histogram was negative, and current MACD histogram is also negative
        macd_signal = "👈"  # MACD histogram is steady or decreasing
    
    else:
        # Default scenario if none of the above conditions are met
        macd_signal = "🫵"  # No significant change in MACD histogram


    return macd_signal



