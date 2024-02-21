import yfinance as yf
import pandas as pd

def sma_above_or_below(symbol):
    # Fetch intraday data
    data = yf.Ticker(symbol).history(period="2d", interval="1m")
    
    # Calculate 50-minute SMA
    data['SMA_50'] = data['Close'].rolling(window=50).mean()
    
    # Get the last row (latest data)
    last_row = data.iloc[-1]
    
    # Get the latest closing price and 50-minute SMA
    latest_price = last_row['Close']
    sma_50 = last_row['SMA_50']
    
    # Check if the latest price is above or below the 50-minute SMA
    if latest_price > sma_50:
        smafifty = "above"
    elif latest_price < sma_50:
        smafifty = "below"
    else:
        smafifty = "equal to"
    
    return smafifty

# Example usage
symbol = "^NSEI"  # NSE Nifty 50 index
sma_fifty_status = sma_above_or_below(symbol)
print(f"The current price of {symbol} is {sma_fifty_status} the 50-minute SMA.")
