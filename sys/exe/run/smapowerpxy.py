import yfinance as yf
import warnings

def check_smapower_status(symbol):
    try:
        # Retrieve historical price data for the given symbol
        data = yf.Ticker(symbol).history(period="5d", interval="1m")

        # Calculate the 50-day SMA of the given symbol
        sma_50 = data['Close'].rolling(window=50).mean()

        # Get the present close price of the given symbol
        present_close = data['Close'].iloc[-1]
        # Suppress FutureWarning temporarily for this section
        with warnings.catch_warnings():
            warnings.simplefilter(action='ignore', category=FutureWarning)
            # Calculate cepower with a maximum of 5
            cepower = min((((present_close) - (sma_50)) / (sma_50)) * 10000, 5)
            # Calculate pepower with a maximum of 5
            pepower = min((((sma_50) - (present_close)) / (sma_50)) * 10000, 5)
            return cepower, pepower  # Return both cepower and pepower as a tuple
    except Exception as e:
        print(f"Error: {e}")
        return None, None  # Return None for both cepower and pepower if an error occurs

# Call the function with a symbol
symbol = "^NSEI"
cepower, pepower = check_smapower_status(symbol)
if cepower is not None and pepower is not None:
    print("cepower:", cepower)
    print("pepower:", pepower)

    

