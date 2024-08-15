import yfinance as yf
import pandas as pd

def fetch_data(symbol, period="1d", interval="1m"):
    """
    Fetch real-time data for the specified interval and symbol.
    """
    data = yf.Ticker(symbol).history(period=period, interval=interval)
    return data

def calculate_heikin_ashi_signals(symbol):
    """
    Fetch data for the symbol, calculate Heikin-Ashi candles, and determine the trading signal.
    """
    data = fetch_data(symbol)
    
    # Calculate Heikin-Ashi close and open
    ha_close = (data['Open'] + data['High'] + data['Low'] + data['Close']) / 4
    ha_open = (data['Open'].shift(1) + data['Close'].shift(1)) / 2

    # Determine the color of the last and previous Heikin-Ashi candles
    current_color = 'Bull' if ha_close.iloc[-1] > ha_open.iloc[-1] else 'Bear'
    last_color = 'Bull' if ha_close.iloc[-2] > ha_open.iloc[-2] else 'Bear'

    # Determine the trading signal based on the color change
    if current_color == 'Bull' and last_color == 'Bull':
        return "Bull"
    elif current_color == 'Bear' and last_color == 'Bear':
        return "Bear"
    elif current_color == 'Bull' and last_color == 'Bear':
        return "Buy"
    elif current_color == 'Bear' and last_color == 'Bull':
        return "Sell"
    else:
        return "None"

def main():
    ticker_symbol = '^NSEI'  # Replace with the actual ticker symbol
    signal = calculate_heikin_ashi_signals(ticker_symbol)
    
    # Print the HA signal as `Buy`, `Sell`, `Bull`, `Bear`, or `None`
    print(f"Signal = {signal}")

if __name__ == "__main__":
    main()

