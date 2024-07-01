import pandas as pd
import yfinance as yf

# Read the CSV file containing the NSE codes
csv_file = 'bankspxy.csv'
df = pd.read_csv(csv_file)

# Assuming the CSV file has a single column with header 'NSE Code'
nse_codes = df['NSE Code'].tolist()

# Dictionary to store current prices
current_prices = {}

# Fetch current prices for each NSE code
for code in nse_codes:
    ticker = f"{code}.NS"  # Append .NS to indicate NSE
    stock = yf.Ticker(ticker)
    history = stock.history(period='1d')
    if not history.empty:
        current_price = history['Close'].iloc[0]
        current_prices[code] = current_price

# Print the current prices
for code, price in current_prices.items():
    print(f"{code}: {price}")
