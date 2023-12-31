import pandas as pd
import yfinance as yf


# Intervals
interval = 5
period = 6

def analyze_stock(symbol):
    try:
        # Append ".NS" to the symbol to specify the NSE exchange
        symbol_with_exchange = symbol + ".NS"

        data = yf.Ticker(symbol).history(period=f'{period[0]}d', interval=f'{interval}m')

        # Calculate Heikin-Ashi candles
        data['HA_Close'] = (data['Open'] + data['High'] + data['Low'] + data['Close']) / 4
        data['HA_Open'] = (data['Open'].shift(1) + data['Close'].shift(1)) / 2

        # Check if yesterday's candle is red and today's candle is green
        yesterday_ha_close = data['HA_Close'].iloc[-2]
        yesterday_ha_open = data['HA_Open'].iloc[-2]
        today_ha_close = data['HA_Close'].iloc[-1]
        today_ha_open = data['HA_Open'].iloc[-1]

        if yesterday_ha_close < yesterday_ha_open and today_ha_close > today_ha_open:
            # Check if the last 5-minute candle today is red and the current candle is green
            last_5min_ha_close = data['HA_Close'].iloc[-2]
            last_5min_ha_open = data['HA_Open'].iloc[-2]
            current_ha_close = data['HA_Close'].iloc[-1]
            current_ha_open = data['HA_Open'].iloc[-1]

            if last_5min_ha_close < last_5min_ha_open and current_ha_close > current_ha_open:
                return 'Buy'
            else:
                return 'Hold'
        else:
            return 'Hold'

    except Exception as e:
        print(f"Error during data download for {symbol}: {e}")
        return 'Error'

# Read symbols from CSV file
df_yxp500 = pd.read_csv('yxp500.csv')
df_HPdf = pd.read_csv('fileHPdf.csv')

# Use 'tradingsymbol' as the column name
symbol_list_yxp500 = df_yxp500['tradingsymbol'].tolist()

# Exclude symbols from fileHPdf.csv
symbol_list_to_analyze = [symbol for symbol in symbol_list_yxp500 if symbol not in df_HPdf['tradingsymbol'].tolist()]

# Analyze each symbol
for symbol in symbol_list_to_analyze:
    decision = analyze_stock(symbol)
    print(f"Decision for {symbol}: {decision}")

