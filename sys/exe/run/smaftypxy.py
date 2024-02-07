import yfinance as yf
import warnings

# Step 1: Retrieve historical price data for Nifty50

data = yf.Ticker('^NSEI').history(period="5d", interval="5m")
# Step 2: Calculate the 50-day SMA of Nifty50
sma_50_nifty = data['Close'].rolling(window=50).mean()

# Step 3: Get the present Nifty close
present_nifty_close = data['Close'].iloc[-1]

# Step 4: Suppress FutureWarning temporarily for this section
with warnings.catch_warnings():
    warnings.simplefilter(action='ignore', category=FutureWarning)

    # Step 5: Compare present Nifty close with 50-day SMA of Nifty50
    if present_nifty_close > sma_50_nifty.iloc[-1]:
        print("NIFTYBULL")
    else:
        print("NIFTYBEAR")
