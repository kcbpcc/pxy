import pandas as pd
import numpy as np
from asciichartpy import plot
from clorpxy import SILVER, BRIGHT_RED, BRIGHT_GREEN, RESET
import yfinance as yf

# Reset terminal color to default
print(RESET)

# Define the ticker symbol for NIFTY
ticker_symbol = "^NSEI"

# Download data from Yahoo Finance
nifty_data = yf.download(ticker_symbol, interval="5m")

# Convert the data to a DataFrame
df = pd.DataFrame(nifty_data['Close'])

# Calculate trend direction
trend_direction = []
for i in range(1, len(df)):
    if df['Close'][i] > df['Close'][i - 1]:
        trend_direction.append(BRIGHT_GREEN)
    elif df['Close'][i] < df['Close'][i - 1]:
        trend_direction.append(BRIGHT_RED)
    else:
        trend_direction.append(SILVER)

# Create ASCII chart with colored trend
chart = plot(df['Close'].tolist(), {'height': 20, 'format': "{:.2f}", 'color': trend_direction})

# Print ASCII chart
print(chart)

# Calculate delta
latest_record = df['Close'].iloc[-1]
previous_record = df['Close'].iloc[-2]
delta = int((latest_record - previous_record) * 100)
delta_color = BRIGHT_GREEN if delta >= 0 else BRIGHT_RED

# Print delta
print("📊📊📊📊📊📊 Delta: {}{}📊📊📊📊📊📊".format(delta_color, str(delta).zfill(10)))

# Reset terminal color to default
print(RESET)
