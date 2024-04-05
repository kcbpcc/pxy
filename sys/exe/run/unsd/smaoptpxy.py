import yfinance as yf
import pandas as pd
def sma_above_or_below(symbol):
    # Fetch intraday data
    data = yf.Ticker(symbol).history(period="2d", interval="1m")
    # Calculate 50-minute SMA
    data['SMA_50'] = data['Close'].rolling(window=50).mean()
    data['SMA_100'] = data['Close'].rolling(window=100).mean()
    # Get the last row (latest data)
    last_row = data.iloc[-1]
    # Get the latest closing price and 50-minute SMA
    sma_1 = last_row['Close']
    sma_50 = last_row['SMA_50']
    sma_100 = last_row['SMA_100']
    # Check if the latest price is above or below the 50-minute SMA
    if sma_1 > sma_100:
        smaopt= "above"
    elif sma_1 < sma_100:
        smaopt= "below"
    else:
        smaopt= "middle"
    return smaopt
