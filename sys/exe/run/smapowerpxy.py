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

            smapower = (((present_close) - (sma_50.iloc[-1]))/ (sma_50.iloc[-1]))*100

            return smapower

    except Exception as e:
        return f"Error: {e}"



