import pandas as pd
import numpy as np
from asciichartpy import plot
from clorpxy import SILVER, BRIGHT_RED, BRIGHT_GREEN, RESET
import yfinance as yf

# Reset terminal color to default
print(RESET)

# Define the ticker symbol for NIFTY
ticker_symbol = "^NSEI"

# Get data from Yahoo Finance for the last 50 days
nifty_data = yf.Ticker(ticker_symbol)

# Fetch historical data
nifty_hist = nifty_data.history(period="50d", interval="1d")

# Calculate Heikin-Ashi (HA) close prices
ha_close = (nifty_hist['Open'] + nifty_hist['High'] + nifty_hist['Low'] + nifty_hist['Close']) / 4

# Calculate Heikin-Ashi (HA) open prices
ha_open = (nifty_hist['Open'].shift(1) + nifty_hist['Close'].shift(1)) / 2

# Calculate trend direction based on HA open-close
trend_direction = []
for i in range(1, len(ha_close)):
    if ha_close.iloc[i] > ha_open.iloc[i]:
        trend_direction.append(BRIGHT_GREEN)
    elif ha_close.iloc[i] < ha_open.iloc[i]:
        trend_direction.append(BRIGHT_RED)
    else:
        trend_direction.append(SILVER)

# Calculate 50-day SMA
sma_50 = ha_close.rolling(window=50).mean().dropna()

# Create ASCII chart with colored trend and SMA line
chart = plot(ha_close.tolist(), {'height': 10, 'format': "{:.0f}", 'color': trend_direction}, sma_50.tolist())

# Print ASCII chart
print(chart)

# Reset terminal color to default
print(RESET)
