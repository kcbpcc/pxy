import yfinance as yf
import os
import sys

def analyze_stock(symbol):
    try:
        # Download historical data for the last 2 days
        data = yf.download(symbol, period="2d")

        # Calculate Heikin-Ashi candles
        data['HA_Close'] = (data['Open'] + data['High'] + data['Low'] + data['Close']) / 4
        data['HA_Open'] = (data['Open'].shift(1) + data['Close'].shift(1)) / 2
        data['HA_High'] = data[['High', 'HA_Open', 'HA_Close']].max(axis=1)
        data['HA_Low'] = data[['Low', 'HA_Open', 'HA_Close']].min(axis=1)

        # Extract yesterday's and today's Heikin-Ashi values
        yesterday_ha_open = data['HA_Open'].iloc[-2]
        yesterday_ha_close = data['HA_Close'].iloc[-2]
        today_ha_open = data['HA_Open'].iloc[-1]
        today_ha_close = data['HA_Close'].iloc[-1]

        # Implement your conditions for buying or selling
        if today_ha_open > today_ha_close > yesterday_ha_open and today_ha_open > yesterday_ha_open:
            return 'Buy'
        elif today_ha_open < today_ha_close < yesterday_ha_open and today_ha_open < yesterday_ha_open:
            return 'Sell'
        else:
            return 'Hold'

    except Exception as e:
        print(f"Error during data download: {e}")
        return 'Error'

# Example of how to use the function
symbol = 'AAPL'
decision = analyze_stock(symbol)
print(f"Decision for {symbol}: {decision}")
