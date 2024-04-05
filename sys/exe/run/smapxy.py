import yfinance as yf
import warnings

def check_index_status(index_symbol):
    # Download historical data
    data = yf.Ticker(index_symbol).history(period="5d", interval="1m")

    # Calculate SMA
    data['50SMA'] = data['Close'].rolling(window=50).mean()
    data['200SMA'] = data['Close'].rolling(window=200).mean()

    # Get the last values of SMA and current price
    last_50sma = data['50SMA'].iloc[-1]
    last_200sma = data['200SMA'].iloc[-1]
    current_price = data['Close'].iloc[-1]

    # Check trend
    if current_price > last_50sma :
        return "up"
    elif current_price < last_50sma :
        return "down"
    else:
        return "side"
