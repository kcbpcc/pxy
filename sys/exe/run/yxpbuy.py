import yfinance as yf

def analyze_stock(symbol):
    try:
        # Download historical data for the last 2 days with 1-minute intervals
        data = yf.download(symbol, period="2d", interval="1m")

        # Calculate Heikin-Ashi candles
        data['HA_Close'] = (data['Open'] + data['High'] + data['Low'] + data['Close']) / 4
        data['HA_Open'] = (data['Open'].shift(1) + data['Close'].shift(1)) / 2
        data['HA_High'] = data[['High', 'HA_Open', 'HA_Close']].max(axis=1)
        data['HA_Low'] = data[['Low', 'HA_Open', 'HA_Close']].min(axis=1)

        # Check if yesterday's candle is red and today's candle is green
        yesterday_ha_close = data['HA_Close'].iloc[-2]
        yesterday_ha_open = data['HA_Open'].iloc[-2]
        today_ha_close = data['HA_Close'].iloc[-1]
        today_ha_open = data['HA_Open'].iloc[-1]

        if yesterday_ha_close > yesterday_ha_open and today_ha_close < today_ha_open:
            # Check if the last 5-minute candle today is red and the current candle is green
            last_5min_ha_close = data['HA_Close'].iloc[-2]
            last_5min_ha_open = data['HA_Open'].iloc[-2]
            current_ha_close = data['HA_Close'].iloc[-1]
            current_ha_open = data['HA_Open'].iloc[-1]

            if last_5min_ha_close > last_5min_ha_open and current_ha_close < current_ha_open:
                return 'Buy'
            else:
                return 'Hold'
        else:
            return 'Hold'

    except Exception as e:
        print(f"Error during data download: {e}")
        return 'Error'

# Example of how to use the function
symbol = 'AAPL'
decision = analyze_stock(symbol)
print(f"Decision for {symbol}: {decision}")

