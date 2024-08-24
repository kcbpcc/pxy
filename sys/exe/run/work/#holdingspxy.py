import sys
import traceback
import pandas as pd
from login_get_kite import get_kite, remove_token
from cnstpxy import dir_path
from toolkit.logger import Logger
import csv
import os
import sys
import traceback
import logging

logging = Logger(30, dir_path + "main.log")

def get_holdingsinfo(resp_list, broker):
    try:
        df = pd.DataFrame(resp_list)
        df['source'] = 'holdings'
        return df
    except Exception as e:
        print(f"An error occurred in holdings: {e}")
        return None

try:
    sys.stdout = open('output.txt', 'w')
    broker = get_kite(api="bypass", sec_dir=dir_path)
except Exception as e:
    remove_token(dir_path)
    print(traceback.format_exc())
    logging.error(f"{str(e)} unable to get holdings")
    sys.exit(1)
finally:
    # Ensure to close the file and restore stdout
    if sys.stdout != sys.__stdout__:
        sys.stdout.close()
        sys.stdout = sys.__stdout__

def process_data():
    try:
        holdings_response = broker.kite.holdings()
        holdings_df = get_holdingsinfo(holdings_response, broker)

        # Save holdings_df to holdings.csv
        holdings_df.to_csv('holdings.csv', index=False)

        holdings_df['key'] = holdings_df['exchange'] + ":" + holdings_df['tradingsymbol'] if not holdings_df.empty else None
        lst = holdings_df['key'].tolist()
        resp = broker.kite.ohlc(lst)
        dct = {
            k: {
                'ltp': v['ohlc'].get('ltp', v['last_price']),
                'open': v['ohlc']['open'],
                'high': v['ohlc']['high'],
                'low': v['ohlc']['low'],
                'close_price': v['ohlc']['close'],
            }
            for k, v in resp.items()
        }
        holdings_df['ltp'] = holdings_df.apply(lambda row: dct.get(row['key'], {}).get('ltp', row['last_price']), axis=1)
        holdings_df['open'] = holdings_df['key'].map(lambda x: dct.get(x, {}).get('open', 0))
        holdings_df['high'] = holdings_df['key'].map(lambda x: dct.get(x, {}).get('high', 0))
        holdings_df['low'] = holdings_df['key'].map(lambda x: dct.get(x, {}).get('low', 0))
        holdings_df['close'] = holdings_df['key'].map(lambda x: dct.get(x, {}).get('close_price', 0))
        holdings_df['qty'] = holdings_df.apply(lambda row: int(row['quantity'] + row['t1_quantity']), axis=1)
        holdings_df['oPL%'] = holdings_df.apply(lambda row: round((((row['ltp'] - row['open']) / row['open']) * 100), 2) if row['open'] != 0 else 0, axis=1)
        holdings_df['dPL%'] = holdings_df.apply(lambda row: round((((row['ltp'] - row['close']) / row['close']) * 100), 2) if row['close'] != 0 else 0, axis=1)

        holdings_df['pnl'] = holdings_df['pnl'].astype(int)
        holdings_df['avg'] = holdings_df['average_price']
        holdings_df['Invested'] = (holdings_df['qty'] * holdings_df['avg']).round(0).astype(int)
        holdings_df['value'] = holdings_df['qty'] * holdings_df['ltp']
        holdings_df['PnL'] = (holdings_df['value'] - holdings_df['Invested']).astype(int)
        holdings_df['PL%'] = ((holdings_df['PnL'] / holdings_df['Invested']) * 100).round(2)
        holdings_df['Yvalue'] = holdings_df['qty'] * holdings_df['close']
        holdings_df['dPnL'] = holdings_df['value'] - holdings_df['Yvalue']

        # Handle conversion of 'm2m' column to int if it exists
        if "m2m" in holdings_df.columns:
            try:
                holdings_df['m2m'] = holdings_df['m2m'].astype(int)
            except ValueError:
                # Handle the case where some values cannot be converted to int
                pass

        return holdings_df

    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()
        return None
