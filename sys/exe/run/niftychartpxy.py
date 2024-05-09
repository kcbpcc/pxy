import pandas as pd
import numpy as np
from asciichartpy import plot
from clorpxy import SILVER, BRIGHT_RED, BRIGHT_GREEN, RESET
import yfinance as yf

# Define the ticker symbol for NIFTY
ticker_symbol = "^NSEI"

# Get data from Yahoo Finance for the last 2 days (to ensure yesterday's close is included)
nifty_data = yf.Ticker(ticker_symbol)
nifty_hist = nifty_data.history(period="2d", interval="1m")

# Extract yesterday's close price
yesterday_close = nifty_hist['Close'].iloc[-1440]  # Assuming 1440 minutes in a day

# Extract today's open price
today_open = nifty_hist['Open'].iloc[0]

# Calculate Heikin-Ashi (HA) close prices for 1-minute candles
ha_close = (nifty_hist['Open'] + nifty_hist['High'] + nifty_hist['Low'] + nifty_hist['Close']) / 4

# Initialize variables
data_points = [yesterday_close, today_open]
ha_15min = None

# Iterate over HA close prices to create 15-minute HA candles
for i in range(2, len(ha_close)):
    if len(data_points) == 17:  # Last 15 data points are 1-minute close prices
        data_points = data_points[:-15]
        data_points.extend(ha_close.iloc[i-15:i].tolist())
    elif len(data_points) == 2:  # First two data points (yesterday close, today open)
        data_points.append(ha_close.iloc[i])
    elif len(data_points) == 16:  # Calculate the first 15-minute HA candle
        ha_15min = np.mean(data_points[-15:])
        data_points.append(ha_15min)
    else:  # Remaining 1-minute data points
        if ha_15min is None:
            ha_15min = np.mean(data_points[-15:])
        else:
            ha_15min = (ha_15min + ha_close.iloc[i]) / 2
        data_points.append(ha_15min)

# Create ASCII chart with colored trend
chart = plot(data_points, {'height': 12, 'format': "{:.0f}"})

# Print ASCII chart
print(chart)

# Reset terminal color to default
print(RESET)




