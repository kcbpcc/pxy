import yfinance as yf
import pandas as pd

def fetch_data(symbol, period="1d", interval="1m"):
    """
    Fetch real-time data for the specified interval and symbol.
    """
    data = yf.Ticker(symbol).history(period=period, interval=interval)
    return data

def calculate_macd(symbol):
    """
    Fetch data for the symbol and calculate the MACD values to determine the trend.
    """
    data = fetch_data(symbol)
    exp1 = data['Close'].ewm(span=12, adjust=False).mean()
    exp2 = data['Close'].ewm(span=26, adjust=False).mean()
    macd = exp1 - exp2
    signal = macd.ewm(span=9, adjust=False).mean()
    macd_trend = "Up" if macd.iloc[-1] > signal.iloc[-1] else "Down"
    return macd_trend

def main():
    ticker_symbol = '^NSEI'  # Replace with the actual ticker symbol
    macd_trend = calculate_macd(ticker_symbol)
    
    # Print the MACD trend as `macd = Up` or `macd = Down`
    print(f"macd = {macd_trend}")

if __name__ == "__main__":
    main()

