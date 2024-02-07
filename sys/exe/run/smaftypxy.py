import yfinance as yf
import warnings

# Suppress FutureWarning
warnings.simplefilter(action='ignore', category=FutureWarning)

# Step 1: Retrieve historical price data for Nifty50
nifty_ticker = yf.Ticker("^NSEI")
data = nifty_ticker.history(period='1d', interval='1d')

# Step 2: Calculate the 50-day SMA of Nifty50
sma_50_nifty = data['Close'].rolling(window=50).mean()

# Step 3: Get the present Nifty close
present_nifty_close = data['Close'].iloc[-1]

# Step 4: Compare present Nifty close with 50-day SMA of Nifty50
if present_nifty_close > sma_50_nifty.iloc[-1]:
    print("50NIFTY")
else:
    print("NIFTY50")
