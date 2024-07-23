import yfinance as yf
import pandas as pd

def get_daily_vix_data(ticker, period):
    vix = yf.Ticker(ticker)
    # Fetch daily data (period options: '1d', '5d', '1mo', '3mo', etc.)
    data = vix.history(period=period)
    return data

def main():
    # Ticker for India VIX
    india_vix_ticker = "^INDIAVIX"
    period = "1mo"  # Last month

    # Fetch daily VIX data
    vix_data = get_daily_vix_data(india_vix_ticker, period)

    # Display the daily data
    print(f"India VIX Data for the Last {period}:")
    print(vix_data)

if __name__ == "__main__":
    main()
