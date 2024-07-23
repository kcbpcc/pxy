import yfinance as yf

# Define the ticker for Nifty index
index_symbol = '^NSEI'  # Or use 'NSEI' if '^NSEI' does not work

# Fetch historical 1-minute data for the last 5 days
data = yf.Ticker(index_symbol).history(period="5d", interval="1m")

# Check if data is fetched correctly
if data.empty:
    print("No data fetched. Please check the ticker symbol or date range.")
else:
    # Calculate the 50-period SMA (50 minutes in this case)
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
