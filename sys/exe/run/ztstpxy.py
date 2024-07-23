import yfinance as yf
import pandas as pd

# Define the ticker for Nifty index
ticker = '^NSEI'  # Or use 'NSEI' if '^NSEI' does not work

# Fetch historical 1-minute data
data = yf.download(ticker, period='2d', interval='1m')  # Fetch data for the last 2 days with 1-minute intervals

# Check if data is fetched correctly
if data.empty:
    print("No data fetched. Please check the ticker symbol or date range.")
else:
    # Calculate the 50-period SMA
    data['SMA50'] = data['Close'].rolling(window=50).mean()

    # Get the most recent data point
    latest_data = data.iloc[-1]
    nifty_price = latest_data['Close']
    sma50_price = latest_data['SMA50']

    # Calculate the difference
    difference = nifty_price - sma50_price

    # Print the results
    print(f"Nifty Index Price: {nifty_price:.2f}")
    print(f"SMA50 Price: {sma50_price:.2f}")
    print(f"Difference: {difference:.2f}")
