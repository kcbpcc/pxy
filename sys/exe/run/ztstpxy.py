import yfinance as yf

# Define the ticker symbol
ticker_symbol = "NIFTY2!"

# Fetch the ticker data
ticker_data = yf.Ticker(ticker_symbol)

# Attempt to retrieve the historical data
try:
    data = ticker_data.history(period="1d")
    if not data.empty:
        current_price = data['Close'].iloc[-1]
        print(f"Current price of {ticker_symbol}: {current_price}")
    else:
        print(f"No data found for symbol {ticker_symbol}. Please check the ticker symbol.")
except IndexError:
    print(f"No data available for {ticker_symbol}.")
except Exception as e:
    print(f"An error occurred: {e}")
