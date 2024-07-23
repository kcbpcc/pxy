import yfinance as yf
import pandas as pd

def get_hourly_vix_data(ticker, hours):
    vix = yf.Ticker(ticker)
    end_time = pd.Timestamp.now()
    start_time = end_time - pd.Timedelta(hours=hours)
    
    # Fetch hourly data (Yahoo Finance might provide data in different intervals)
    data = vix.history(start=start_time, end=end_time, interval="1h")
    return data

def main():
    # Ticker for India VIX
    india_vix_ticker = "^INDIAVIX"
    hours = 10

    # Fetch hourly VIX data
    vix_data = get_hourly_vix_data(india_vix_ticker, hours)

    # Display the hourly data
    print("India VIX Data for the Last 10 Hours:")
    print(vix_data)

if __name__ == "__main__":
    main()
