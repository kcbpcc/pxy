from rich import print
import sys
import yfinance as yf
import pandas as pd

def get_nse_action():
    try:
        # Download data for a fixed 7-day period
        data = yf.Ticker('^NSEI').history(period="7d")
        ha_data = pd.DataFrame(index=data.index)

        # Calculate Heikin-Ashi (HA) candles
        ha_data['Close'] = (data['Open'] + data['High'] + data['Low'] + data['Close']) / 4
        ha_data['Open'] = (ha_data['Close'].shift(1) + ha_data['Open'].shift(1)) / 2

        ha_data['High'] = ha_data[['Open', 'Close', 'High']].max(axis=1)
        ha_data['Low'] = ha_data[['Open', 'Close', 'Low']].min(axis=1)

        # Extract today's and yesterday's HA candle values
        today_ha_open = ha_data['Open'].iloc[-1]
        today_ha_close = ha_data['Close'].iloc[-1]
        yesterday_ha_open = ha_data['Open'].iloc[-2]
        yesterday_ha_close = ha_data['Close'].iloc[-2]

        # Determine if today's candle is bullish or bearish compared to yesterday
        nse_action = ""
        OPTIONS = None
        if today_ha_close > today_ha_open:
            nse_action = "Bullish"
            OPTIONS = round(data['Close'].iloc[-1] / 50) * 50 if data['Close'].iloc[-1] % 100 < 50 else round(data['Close'].iloc[-1] / 100) * 100
        elif today_ha_close < today_ha_open:
            nse_action = "Bearish"
            OPTIONS = round(data['Close'].iloc[-1] / 50) * 50 if data['Close'].iloc[-1] % 100 < 50 else round(data['Close'].iloc[-1] / 100) * 100
        else:
            nse_action = 'Neutral'

        # Calculate nse_power
        raw_nse_power = (data['Close'].iloc[-1] - (data['Low'].iloc[-1] - 0.01)) / (abs(data['High'].iloc[-1] + 0.01) - abs(data['Low'].iloc[-1] - 0.01))
        nse_power = round(max(0.1, min(raw_nse_power, 1.0)), 2)
        Day_Change = round(((data['Close'].iloc[-1] - data['Close'].iloc[-2]) / data['Close'].iloc[-2]) * 100, 2)
        Open_Change = round(((data['Close'].iloc[-1] - data['Open'].iloc[-1]) / data['Open'].iloc[-1]) * 100, 2)

        return nse_action, nse_power, Day_Change, Open_Change, OPTIONS

    except Exception as e:
        print(f"Error occurred: {e}")
        return None, None, None, None, None

# Call the get_nse_action function
nse_action, nse_power, Day_Change, Open_Change, OPTIONS = get_nse_action()
if nse_action is not None:
    print("NSE Action:", nse_action)
    print("NSE Power:", nse_power)
    print("Day Change:", Day_Change)
    print("Open Change:", Open_Change)
    print("OPTIONS:", OPTIONS)
