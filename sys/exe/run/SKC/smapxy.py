# sma50pxy.py
import yfinance as yf
import pandas as pd

def fetch_data(symbol, period="1d", interval="1m"):
    """
    Fetch real-time data for the specified interval and symbol.
    """
    data = yf.Ticker(symbol).history(period=period, interval=interval)
    return data

def calculate_sma50(data):
    """
    Calculate the 50-period SMA and determine if the current price is above or below it.
    """
    data['50SMA'] = data['Close'].rolling(window=50).mean()
    current_price = data['Close'].iloc[-1]
    sma50_value = data['50SMA'].iloc[-1]
    is_above = current_price > sma50_value
    return "Up" if is_above else "Down"

def main():
    ticker_symbol = '^NSEI'  # Replace with the actual ticker symbol
    data = fetch_data(ticker_symbol)
    sma_trend = calculate_sma50(data)
    
    # Print the SMA trend as `sma = Up` or `sma = Down`
    print(f"sma = {sma_trend}")

if __name__ == "__main__":
    main()
