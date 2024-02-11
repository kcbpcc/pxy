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
            cepower = (((present_close) - (sma_50.iloc[-1]))/ (sma_50.iloc[-1]))*10000
            pepower = (((sma_50.iloc[-1]) - (present_close))/ (sma_50.iloc[-1]))*10000
            return cepower
            return pepower
    except Exception as e:
        print(f"Error: {e}")
        return None  # Return None if an error occurs

# Call the function with a symbol
symbol = "^NSEI"
pepower, cepower = check_smapower_status(symbol)
if smapower is not None:
    print("cepower:", cepower)
    print("pepower:", pepower)
    

