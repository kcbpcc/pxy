import yfinance as yf

# Define the ticker symbols
ticker_symbols = ["IND50", "NIFc1", "NIFc2", "NIFc3"]

# Iterate over each symbol and attempt to retrieve the price
for ticker_symbol in ticker_symbols:
    print(f"\nChecking data for symbol: {ticker_symbol}")
    
    ticker_data = yf.Ticker(ticker_symbol)
    
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
