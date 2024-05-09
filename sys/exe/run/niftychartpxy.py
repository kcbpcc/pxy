import pandas as pd
import numpy as np
from asciichartpy import plot
from clorpxy import SILVER, BRIGHT_RED, BRIGHT_GREEN, RESET
import yfinance as yf

# Define the ticker symbol for NIFTY
ticker_symbol = "^NSEI"

# Download data for a fixed 7-day period
data = yf.Ticker(ticker_symbol).history(period="7d")

# Extract today's open, yesterday's close, and current price
today_open = data['Open'].iloc[-1]
yesterday_close = data['Close'].iloc[-2]

# Get data from Yahoo Finance for the last 2 days (to ensure enough data for 15-minute candles)
nifty_data = yf.Ticker(ticker_symbol)
nifty_hist = nifty_data.history(period="2d", interval="1m")

# Extract close prices for 1-minute candles
close_1min = nifty_hist['Close'].tolist()

# Calculate close prices for 15-minute candles
close_15min = nifty_hist['Close'].resample('15min').ohlc()['close'].dropna().tolist()

# Extract the last 15 1-minute close prices
last_1min_close = close_1min[-15:]

# Extract the last 20 15-minute close prices
last_20_15min_close = close_15min[-22:-2]  # Excluding the last one

# Combine the last 20 15-minute close prices and the last 15 1-minute close prices
data_points = last_20_15min_close + last_1min_close

# Create ASCII chart with colored trend
chart = plot(data_points, {'height': 12, 'format': "{:.0f}"})

# Add color indicators for yesterday's close and today's open on Y-axis
chart = chart.replace(str(int(yesterday_close)), BRIGHT_RED + str(int(yesterday_close)) + RESET)
chart = chart.replace(str(int(today_open)), BRIGHT_GREEN + str(int(today_open)) + RESET)

# Print ASCII chart
print(chart)

# Reset terminal color to default
print(RESET)
