import pandas as pd
import numpy as np
from asciichartpy import plot
from clorpxy import SILVER, BRIGHT_RED, BRIGHT_GREEN, RESET
import yfinance as yf

# Reset terminal color to default
print(RESET)

# Define the ticker symbol for NIFTY
ticker_symbol = "^NSEI"

# Get data from Yahoo Finance for the last 2.5 hours
nifty_data = yf.Ticker(ticker_symbol)

# Fetch historical data
nifty_hist = nifty_data.history(period="1d", interval="15m")

# Fetch latest data (current 15-minute interval)
latest_data = nifty_hist.iloc[-1]

# Calculate Heikin-Ashi (HA) close prices
ha_close = (latest_data['Open'] + latest_data['High'] + latest_data['Low'] + latest_data['Close']) / 4

# Calculate Heikin-Ashi (HA) open prices
ha_open = (latest_data['Open'] + latest_data['Close']) / 2

# Calculate trend direction based on HA open-close
if ha_close > ha_open:
    trend_direction = BRIGHT_GREEN
elif ha_close < ha_open:
    trend_direction = BRIGHT_RED
else:
    trend_direction = SILVER

# Create ASCII chart with colored trend for the latest 15-minute interval
chart = plot([ha_close], {'height': 10, 'format': "{:.0f}", 'color': [trend_direction]})

# Print ASCII chart
print(chart)

# Reset terminal color to default
print(RESET)
