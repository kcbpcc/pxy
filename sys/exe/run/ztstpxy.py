import yfinance as yf

# Define the ticker symbol
ticker_symbol = "NIFTY1!"

# Fetch the ticker data
ticker_data = yf.Ticker(ticker_symbol)

# Get the last available market price
current_price = ticker_data.history(period="1d")['Close'].iloc[-1]

# Print the current price
print(f"Current price of {ticker_symbol}: {current_price}")

