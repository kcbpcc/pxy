import pandas as pd
import numpy as np
from asciichartpy import plot
from clorpxy import SILVER, BRIGHT_RED, BRIGHT_GREEN, RESET
import yfinance as yf

# Define the ticker symbol for NIFTY
ticker_symbol = "^NSEI"

# Get data from Yahoo Finance for the last 5 days
nifty_data = yf.Ticker(ticker_symbol)

# Fetch historical data
nifty_hist = nifty_data.history(period="5d", interval="60m")[-35:]

# Calculate Heikin-Ashi (HA) close prices for all data points
ha_close = (nifty_hist['Open'] + nifty_hist['High'] + nifty_hist['Low'] + nifty_hist['Close']) / 4

# Calculate Heikin-Ashi (HA) open prices
ha_open = (nifty_hist['Open'].shift(1) + nifty_hist['Close'].shift(1)) / 2

# Calculate trend direction based on HA open-close
trend_direction = []
for i in range(1, len(ha_close)):
    if ha_close.iloc[i] > ha_open.iloc[i]:
        trend_direction.append(BRIGHT_GREEN + "█")
    elif ha_close.iloc[i] < ha_open.iloc[i]:
        trend_direction.append(BRIGHT_RED + "█")
    else:
        trend_direction.append(SILVER + "█")

# Extract last close price for plain close price
latest_close_price = nifty_hist['Close'].iloc[-1]

# Create ASCII chart with colored trend
chart = plot(ha_close.tolist()[:-1] + [latest_close_price], {'height': 20, 'format': "{:.0f}"})

# Apply trend direction colors to chart
for i, color in enumerate(trend_direction):
    chart = chart.replace("█", color, 1)

# Print ASCII chart
print(chart)

# Reset terminal color to default
print(RESET)


