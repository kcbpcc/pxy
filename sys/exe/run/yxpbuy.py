from toolkit.logger import Logger
from toolkit.currency import round_to_paise
from toolkit.utilities import Utilities
from login_get_kite import get_kite
from cnstpxy import dir_path, fileutils, buybuff, max_target
import pandas as pd
import traceback
import sys
from fundpxy import calculate_decision
from mktpxy import get_market_check
import logging
import yfinance as yf
from smbpxy import get_smbpxy_check
from nftpxy import nse_action

mktchk = get_market_check('^NSEI')
logging = Logger(10)

black_file = dir_path + "blacklist.txt"

try:
    sys.stdout = open('output.txt', 'w')
    broker = get_kite(api="bypass", sec_dir=dir_path)

except Exception as e:
    print(traceback.format_exc())
    sys.exit(1)

# Call the calculate_decision function to get the decision
decision = calculate_decision()

def analyze_stock(symbol):  # Add nse_action as an argument
    try:
        # Append ".NS" to the symbol to specify the NSE exchange
        symbol_with_exchange = symbol + ".NS"
        smbchk = get_smbpxy_check(symbol_with_exchange)

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
        mktpxy = get_market_check(symbol_with_exchange)

        if (
            daybeforeyesterday_close < daybeforeyesterday_open
            and yesterday_close > yesterday_open
            and today_close > today_open
            and (nse_action == 'Bull' or nse_action == 'Bullish')
            and mktchk == 'Buy'
            and smbchk == 'Buy'
        ):
            return 'Buy'
        elif (
            daybeforeyesterday_close > daybeforeyesterday_open
            and yesterday_close < yesterday_open
            and today_close < today_open
            and (nse_action == 'Bear' or nse_action == 'Bearish')
            and mktchk == 'Sell'
            and smbchk == 'Sell'
        ):
            return 'Sell'
        else:
            return 'None'

    except Exception as e:
        print(f"Error during data download for {symbol}: {e}")
        return 'Error'

df_yxp500 = pd.read_csv('yxp500.csv')
df_HPdf = pd.read_csv('fileHPdf.csv')

# Use 'tradingsymbol' as the column name
symbol_list_yxp500 = df_yxp500['tradingsymbol'].tolist()

# Exclude symbols from fileHPdf.csv
symbol_list_to_analyze = [symbol for symbol in symbol_list_yxp500 if symbol not in df_HPdf['tradingsymbol'].tolist()]

# Initialize an empty list to store symbols to sell
symbols_to_sell = []

# Analyze each symbol
for symbol in symbol_list_to_analyze:
    decision = analyze_stock(symbol)  # Pass nse_action as an argument
    print(f"Decision for {symbol}: {decision}")

    # Check if the decision is 'Sell' and append the symbol to the list
    if decision == 'Sell':
        symbols_to_sell.append(symbol)

# Print the list of symbols to sell
print("Symbols to Sell:", symbols_to_sell)




