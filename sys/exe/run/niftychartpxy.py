
import pandas as pd
import numpy as np
from asciichartpy import plot
from clorpxy import SILVER, BRIGHT_RED, BRIGHT_GREEN, RESET
import yfinance as yf
import warnings

# Suppress FutureWarning from yfinance library
warnings.filterwarnings("ignore", message="'T' is deprecated", category=FutureWarning)

# Define the ticker symbol for NIFTY
ticker_symbol = "^NSEI"

# Get data from Yahoo Finance for the last 5 days with different intervals
nifty_data = yf.Ticker(ticker_symbol)

# Fetch historical data for the last 5 periods with 1-hour interval
nifty_hist_1h = nifty_data.history(period="5d", interval="1h")[-5:]

# Fetch historical data for the last 25 periods with 1-minute, 5-minute, 15-minute, and 30-minute intervals
nifty_hist_1m = nifty_data.history(period="5d", interval="1m")[-5:]
nifty_hist_5m = nifty_data.history(period="5d", interval="5m")[-5:]
nifty_hist_15m = nifty_data.history(period="5d", interval="15m")[-5:]
nifty_hist_30m = nifty_data.history(period="5d", interval="30m")[-5:]

# Fetch historical data for the last 5 periods with 1-day interval
nifty_hist_1d = nifty_data.history(period="5d", interval="1d")[-5:]

# Combine all data to get the last 30 data points
nifty_hist = pd.concat([nifty_hist_1d, nifty_hist_1h, nifty_hist_30m, nifty_hist_15m, nifty_hist_5m, nifty_hist_1m])

# Get the close prices
close_prices = nifty_hist['Close']

# Create ASCII chart with colored trend
chart = plot(close_prices.tolist(), {'height': 10, 'format': "{:.0f}"})

# Print ASCII chart
print(chart)

# Reset terminal color to default
print(RESET)

