import yfinance as yf
import pandas as pd

def check_sma_trend(index_symbol):
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
    if current_price > last_50sma and last_50sma > last_200sma:
        return "Price is above 50SMA and 50SMA is above 200SMA (uptrend)"
    elif current_price < last_50sma and last_50sma < last_200sma:
        return "Price is below 50SMA and 50SMA is below 200SMA (downtrend)"
    else:
        return "No clear trend"

if __name__ == "__main__":
    index_symbol = input("Enter the index symbol (e.g., ^GSPC for S&P 500): ")
    result = check_sma_trend(index_symbol)
    print(result)
