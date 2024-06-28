# depthpxy.py

import yfinance as yf
import pandas as pd
import warnings

def calculate_consecutive_candles(tickerSymbol):
    # Suppress warnings
    warnings.filterwarnings("ignore")

    try:
        # Get data on this ticker
        tickerData = yf.Ticker(tickerSymbol)

        # Get the historical prices for this ticker
        tickerDf = tickerData.history(period='5d', interval='1m')

        # Calculate Heiken Ashi candles
        ha_close = (tickerDf['Open'] + tickerDf['High'] + tickerDf['Low'] + tickerDf['Close']) / 4
        ha_open = ha_close.shift(1)
        ha_high = tickerDf[['High', 'Open', 'Close']].max(axis=1)
        ha_low = tickerDf[['Low', 'Open', 'Close']].min(axis=1)

        # Determine Heiken Ashi candle colors
        ha_color = pd.Series('green', index=ha_close.index)
        ha_color[ha_close < ha_open] = 'red'

        # Calculate consecutive candles sequence
        consecutive_count = 1
        current_color = None

        for i in range(1, len(ha_color)):
            if ha_color[i] == ha_color[i - 1]:
                consecutive_count += 1
            else:
                consecutive_count = 1
                current_color = ha_color[i]

        # Calculate cedepth and pedepth
        if current_color is not None:
            if consecutive_count > 9:
                consecutive_count = 9
            if current_color == 'green':
                cedepth = consecutive_count
                pedepth = 1
            else:
                cedepth = 1
                pedepth = consecutive_count
            return cedepth, pedepth
    except Exception as e:
        return f"An error occurred: {e}"
