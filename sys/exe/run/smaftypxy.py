import yfinance as yf
import warnings

def check_nifty_status():
    # Retrieve historical price data for Nifty50
    nifty_ticker = yf.Ticker("^NSEI")
    data = nifty_ticker.history(period='1d', interval='1d')

    # Calculate the 50-day SMA of Nifty50
    sma_50_nifty = data['Close'].rolling(window=50).mean()

    # Get the present Nifty close
    present_nifty_close = data['Close'].iloc[-1]

    # Suppress FutureWarning temporarily for this section
    with warnings.catch_warnings():
        warnings.simplefilter(action='ignore', category=FutureWarning)

        # Compare present Nifty close with 50-day SMA of Nifty50
        if present_nifty_close > sma_50_nifty.iloc[-1]:
            return "50NIFTY"
        else:
            return "NIFTY50"

# Example usage
print(check_nifty_status())
