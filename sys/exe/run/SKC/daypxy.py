# day_metrics.py
import yfinance as yf
import pandas as pd

def fetch_data(symbol, period="5d", interval="1d"):
    """
    Fetch historical daily data for the specified period and symbol.
    """
    data = yf.Ticker(symbol).history(period=period, interval=interval)
    return data

def calculate_day_metrics(symbol, period="5d", interval="1d"):
    """
    Fetch data and calculate Day Change (dayd), Open Change (dayo), and Day Power (dayp).
    """
    # Fetch the historical data
    data = fetch_data(symbol, period, interval)

    # Ensure there are at least two days of data
    if len(data) < 2:
        return "Not enough data"

    today_open = data['Open'].iloc[-1]
    today_high = data['High'].iloc[-1]
    today_low = data['Low'].iloc[-1]
    current_price = data['Close'].iloc[-1]
    yesterday_close = data['Close'].iloc[-2]

    # Calculate Day Change (dayd)
    dayd = round(((current_price - yesterday_close) / yesterday_close) * 100, 2)
    
    # Calculate Open Change (dayo)
    dayo = round(((current_price - today_open) / today_open) * 100, 2)

    # Calculate Day Power (dayp)
    raw_day_power = (current_price - (today_low - 0.01)) / (abs(today_high + 0.01) - abs(today_low - 0.01))
    dayp = round(max(0.1, min(raw_day_power, 1.0)), 2)

    return dayd, dayo, dayp

if __name__ == "__main__":
    # Example usage within the same script
    dayd, dayo, dayp = calculate_day_metrics('^NSEI')
    if isinstance(dayd, str):  # Handling "Not enough data" case
        print(dayd)
    else:
        print(f"Day Change (dayd): {dayd}%")
        print(f"Open Change (dayo): {dayo}%")
        print(f"Day Power (dayp): {dayp}")
