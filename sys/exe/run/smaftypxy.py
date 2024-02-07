import yfinance as yf
import pandas as pd

# Step 1: Retrieve historical price data for Nifty50
nifty_ticker = yf.Ticker("^NSEI")
data = nifty_ticker.history(period='5d', interval='1m')

# Step 2: Calculate the HA candle close
ha_close = (data['Open'] + data['High'] + data['Low'] + data['Close']) / 4

# Step 3: Calculate the 50-day SMA of Nifty50
sma_50_nifty = data['Close'].rolling(window=50).mean()

# Step 4: Compare HA candle close with 50-day SMA of Nifty50
compare_result = ha_close > sma_50_nifty

# Step 5: Print "50NIFTY" if HA candle close is above SMA, otherwise print "NIFTY50"
if compare_result.iloc[-1]:  # Check the most recent value
    print("50NIFTY")
else:
    print("NIFTY50")
