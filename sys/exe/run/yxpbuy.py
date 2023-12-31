import pandas as pd
import yfinance as yf


def analyze_stock(symbol):
    try:
        # Append ".NS" to the symbol to specify the NSE exchange
        symbol_with_exchange = symbol + ".NS"

        # Download historical stock data for the last 2 days with a daily interval
        data = yf.download(symbol_with_exchange, period="7d", interval="1d")
        
        # Calculate Heikin-Ashi candles for daily data
        data['Close'] = data['Close']
        data['Open'] = data['Open']

        # Check if yesterday's candle is red and today's candle is green
        daybeforeyesterday_close = data['Close'].iloc[-3]
        daybeforeyesterday_open = data['Open'].iloc[-3]
        yesterday_close = data['Close'].iloc[-2]
        yesterday_open = data['Open'].iloc[-2]
        today_close = data['Close'].iloc[-1]
        today_open = data['Open'].iloc[-1]

        if daybeforeyesterday_ha_close < daybeforeyesterday_ha_open and yesterday_ha_close > yesterday_ha_open and today_ha_close > today_ha_open:
            return 'Buy'
        elif daybeforeyesterday_ha_close > daybeforeyesterday_ha_open and yesterday_ha_close < yesterday_ha_open and today_ha_close < today_ha_open:
            return 'Sell'
        else:
            return 'None'

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

