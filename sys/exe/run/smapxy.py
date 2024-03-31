import yfinance as yf
import warnings

def check_index_status(index_symbol):
    # Retrieve historical price data for the given index
    data = yf.Ticker(index_symbol).history(period="5d", interval="1m")

    # Calculate the 100-day SMA of the index
    sma_100_index = data['Close'].rolling(window=50).mean()

    # Get the present index close
    present_index_close = data['Close'].iloc[-1]

    # Suppress FutureWarning temporarily for this section
    with warnings.catch_warnings():
        warnings.simplefilter(action='ignore', category=FutureWarning)

        # Compare present index close with 100-day SMA of the index
        if present_index_close > sma_50_index.iloc[-1]:
            return "up"
        else:
            return "down"
