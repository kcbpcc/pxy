import pandas as pd
import numpy as np
from asciichartpy import plot
from clorpxy import SILVER, BRIGHT_RED, BRIGHT_GREEN, RESET
import yfinance as yf

# Define the ticker symbol for NIFTY
ticker_symbol = "^NSEI"

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
last_20_15min_close = close_15min[-22:-2]  # Corrected index to -2

# Combine the last 20 15-minute close prices and the last 15 1-minute close prices
data_points = last_20_15min_close + last_1min_close

# Calculate the 50-period Simple Moving Average (SMA) on 1-minute interval data
sma_50_series = pd.Series(close_1min).rolling(window=50).mean()
sma_50 = sma_50_series.tolist()

# Get the latest SMA value, ensuring it's not NaN
current_sma_50 = sma_50[-1] if pd.notna(sma_50[-1]) else None

# Create ASCII chart with colored trend
chart = plot(data_points, {'height': 12, 'format': "{:.0f}"})

# If SMA value is not None, highlight its approximate position on the scale
if current_sma_50 is not None:
    sma_indicator = f"Current 50 SMA: {current_sma_50:.2f}"
    # Find the approximate position of the SMA on the scale
    chart_lines = chart.split('\n')
    min_value = min(data_points)
    max_value = max(data_points)
    scale_step = (max_value - min_value) / (len(chart_lines) - 1)
    
    for i, line in enumerate(chart_lines):
        line_value = max_value - i * scale_step
        if abs(line_value - current_sma_50) < scale_step / 2:
            # Highlight the scale value
            line_parts = line.split(' ')
            line_parts[0] = f"{BRIGHT_RED}{line_parts[0]}{RESET}"
            chart_lines[i] = ' '.join(line_parts)
    
    highlighted_chart = "\n".join(chart_lines)
    print(highlighted_chart)
    print(sma_indicator)
else:
    print(chart)
    #print("Current 50 SMA: Not enough data to calculate 50 SMA")

# Reset terminal color to default
print(RESET)
