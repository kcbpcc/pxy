import pandas as pd
import numpy as np
from asciichartpy import plot
from clorpxy import SILVER, BRIGHT_RED, BRIGHT_GREEN, RESET
import yfinance as yf
import sys

# Check if terminal supports ANSI color codes
if not hasattr(sys.stdout, "isatty") or not sys.stdout.isatty():
    print("Terminal does not support ANSI color codes. Please use a compatible terminal.")
    sys.exit(1)

# Check if asciichartpy library supports color rendering
if not plot([1, 2], {'color': [BRIGHT_RED, BRIGHT_GREEN]}):
    print("asciichartpy library does not support color rendering. Please check if there's an update.")
    sys.exit(1)

# Reset terminal color to default
print(RESET)

# Define the ticker symbol for NIFTY
ticker_symbol = "^NSEI"

# Get data from Yahoo Finance for the last 2.5 hours
nifty_data = yf.download(ticker_symbol, period="1d", interval="15m")

# Fetch latest data (current 15-minute interval)
latest_data = nifty_data.iloc[-1]

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

