import yfinance as yf
import warnings

def check_smapower_status(symbol):
    try:
        # Retrieve historical price data for the given symbol
        data = yf.Ticker(symbol).history(period="5d", interval="1m")

        # Get the present close price of the given symbol
        present_close = data['Close'].iloc[-1]
        # Calculate the 50-day SMA of the given symbol
        sma_50 = data['Close'].rolling(window=50).mean().iloc[-1]

        # Calculate cepower with a maximum of 5
        pepower = round(max((((sma_50) - (present_close)) / (sma_50)) * 10000, 1.4), 2)
        # Calculate pepower with a maximum of 5
        cepower = round(max((((present_close) - (sma_50)) / (sma_50)) * 10000, 1.4), 2)
        
        return cepower, pepower
    except Exception as e:
        print(f"Error: {e}")
        return None, None  # Return None for both cepower and pepower if an error occurs



    

