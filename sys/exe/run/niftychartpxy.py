import pandas as pd
import numpy as np
from asciichartpy import plot
from clorpxy import SILVER, BRIGHT_RED, BRIGHT_GREEN, RESET
import yfinance as yf

# Reset terminal color to default
print(RESET)

# Define the ticker symbol for NIFTY
ticker_symbol = "^NSEI"

# Get data from Yahoo Finance for the last 2 hours
nifty_data = yf.Ticker(ticker_symbol)

# Fetch historical data
nifty_hist = nifty_data.history(period="2h", interval="5m")

# Select only the 'Close' prices
df = nifty_hist['Close']

# Calculate trend direction
trend_direction = []
for i in range(1, len(df)):
    if df.iloc[i] > df.iloc[i - 1]:
        trend_direction.append(BRIGHT_GREEN)
    elif df.iloc[i] < df.iloc[i - 1]:
        trend_direction.append(BRIGHT_RED)
    else:
        trend_direction.append(SILVER)

# Create ASCII chart with colored trend
chart = plot(df.tolist(), {'height': 10, 'format': "{:.0f}", 'color': trend_direction})

# Print ASCII chart
print(chart)

# Calculate delta
delta = int((today_close - yesterday_close) * 100)
delta_color = BRIGHT_GREEN if delta >= 0 else BRIGHT_RED

# Print delta
print("📊📊📊📊📊📊 Delta: {}{}📊📊📊📊📊📊".format(delta_color, str(delta).zfill(10)))

# Reset terminal color to default
print(RESET)
