import pandas as pd
import numpy as np
from asciichartpy import plot
from clorpxy import SILVER, BRIGHT_RED, BRIGHT_GREEN, RESET
import yfinance as yf

# Define the ticker symbol for NIFTY
ticker_symbol = "^NSEI"

# Get data from Yahoo Finance for the last 6 days (to ensure yesterday's close is included)
nifty_data = yf.Ticker(ticker_symbol)
nifty_hist = nifty_data.history(period="6d", interval="1d")

# Calculate Heikin-Ashi (HA) close prices for 15-minute candles
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

# Extract yesterday's close price for the first data point
yesterday_close = nifty_hist['Close'].iloc[-2]

# Extract latest normal close price for the 35th data point
latest_close_price = nifty_hist['Close'].iloc[-1]

# Get the current close price
current_close_price = nifty_hist['Close'].iloc[-1]

# Get the current datetime
current_datetime = nifty_hist.index[-1]

# Check if the current time is within a 15-minute interval
if current_datetime.minute % 15 == 0:
    # If current time is at the end of a 15-minute interval, use Heikin-Ashi close
    third_data_point = ha_close.iloc[-1]
else:
    # Otherwise, use the current close price
    third_data_point = current_close_price

# Create ASCII chart data
chart_data = [yesterday_close, third_data_point] + ha_close.tolist()[1:33] + [latest_close_price]

# Create ASCII chart with colored trend
chart = plot(chart_data, {'height': 12, 'format': "{:.0f}"})

# Apply trend direction colors to chart
for i, color in enumerate(trend_direction):
    chart = chart.replace("█", color, 1)

# Print ASCII chart
print(chart)

# Reset terminal color to default
print(RESET)




