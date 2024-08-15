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
def get_positionsinfo(resp_list, broker):
    try:
        df = pd.DataFrame(resp_list)
        df['source'] = 'positions'
        return df
    except Exception as e:
        print(f"An error occurred in positions: {e}")
        return None
try:
    sys.stdout = open('output.txt', 'w')
    broker = get_kite()
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
        positions_response = broker.kite.positions()['net']
        holdings_df = get_holdingsinfo(holdings_response, broker)
        holdings_df.to_csv('pxyholdings.csv', index=False)
        positions_df = get_positionsinfo(positions_response, broker)
        positions_df.to_csv('pxypositions.csv', index=False)
        holdings_df['key'] = holdings_df['exchange'] + ":" + holdings_df['tradingsymbol'] if not holdings_df.empty else None
        positions_df['key'] = positions_df['exchange'] + ":" + positions_df['tradingsymbol'] if not positions_df.empty else None
        combined_df = pd.concat([holdings_df, positions_df], ignore_index=True)
        lst = combined_df['key'].tolist()
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
        combined_df['ltp'] = combined_df.apply(lambda row: dct.get(row['key'], {}).get('ltp', row['last_price']), axis=1)
        combined_df['open'] = combined_df['key'].map(lambda x: dct.get(x, {}).get('open', 0))
        combined_df['high'] = combined_df['key'].map(lambda x: dct.get(x, {}).get('high', 0))
        combined_df['low'] = combined_df['key'].map(lambda x: dct.get(x, {}).get('low', 0))
        combined_df['close'] = combined_df['key'].map(lambda x: dct.get(x, {}).get('close_price', 0))
        combined_df['qty'] = combined_df.apply(lambda row: int(row['quantity'] + row['t1_quantity']) if row['source'] == 'holdings' else int(row['quantity']), axis=1)
        combined_df['oPL%'] = combined_df.apply(lambda row: round((((row['ltp'] - row['open']) / row['open']) * 100), 2) if row['open'] != 0 else 0, axis=1)
        combined_df['dPL%'] = combined_df.apply(lambda row: round((((row['ltp'] - row['close']) / row['close']) * 100), 2) if row['close'] != 0 else 0, axis=1)
        combined_df['pnl'] = combined_df['pnl'].astype(int)
        combined_df['avg'] = combined_df['average_price']
        combined_df['Invested'] = (combined_df['qty'] * combined_df['avg']).round(0).astype(int)
        combined_df['value'] = combined_df['qty'] * combined_df['ltp']
        combined_df['PnL'] = (combined_df['value'] - combined_df['Invested']).astype(int)
        combined_df['PL%'] = ((combined_df['PnL'] / combined_df['Invested']) * 100).round(2)
        combined_df['Yvalue'] = combined_df['qty'] * combined_df['close']
        combined_df['dPnL'] = combined_df['value'] - combined_df['Yvalue']
        combined_df.to_csv('pxycombined.csv', index=False)
        return combined_df
    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()
        return None

