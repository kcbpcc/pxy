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
    broker = get_kite(api="bypass", sec_dir=dir_path)
except Exception as e:
    remove_token(dir_path)
    print(traceback.format_exc())
    logging.error(f"{str(e)} unable to get positions")
    sys.exit(1)
finally:
    # Ensure to close the file and restore stdout
    if sys.stdout != sys.__stdout__:
        sys.stdout.close()
        sys.stdout = sys.__stdout__

def process_data():
    try:
        positions_response = broker.kite.positions()['net']
        positions_df = get_positionsinfo(positions_response, broker)

        # Save positions_df to positions.csv
        positions_df.to_csv('positions.csv', index=False)

        positions_df['key'] = positions_df['exchange'] + ":" + positions_df['tradingsymbol'] if not positions_df.empty else None
        lst = positions_df['key'].tolist()
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
        positions_df['ltp'] = positions_df.apply(lambda row: dct.get(row['key'], {}).get('ltp', row['last_price']), axis=1)
        positions_df['open'] = positions_df['key'].map(lambda x: dct.get(x, {}).get('open', 0))
        positions_df['high'] = positions_df['key'].map(lambda x: dct.get(x, {}).get('high', 0))
        positions_df['low'] = positions_df['key'].map(lambda x: dct.get(x, {}).get('low', 0))
        positions_df['close'] = positions_df['key'].map(lambda x: dct.get(x, {}).get('close_price', 0))
        positions_df['qty'] = positions_df.apply(lambda row: int(row['quantity']), axis=1)
        positions_df['oPL%'] = positions_df.apply(lambda row: round((((row['ltp'] - row['open']) / row['open']) * 100), 2) if row['open'] != 0 else 0, axis=1)
        positions_df['dPL%'] = positions_df.apply(lambda row: round((((row['ltp'] - row['close']) / row['close']) * 100), 2) if row['close'] != 0 else 0, axis=1)

        positions_df['pnl'] = positions_df['pnl'].astype(int)
        positions_df['avg'] = positions_df['average_price']
        positions_df['Invested'] = (positions_df['qty'] * positions_df['avg']).round(0).astype(int)
        positions_df['value'] = positions_df['qty'] * positions_df['ltp']
        positions_df['PnL'] = (positions_df['value'] - positions_df['Invested']).astype(int)
        positions_df['PL%'] = ((positions_df['PnL'] / positions_df['Invested']) * 100).round(2)
        positions_df['Yvalue'] = positions_df['qty'] * positions_df['close']
        positions_df['dPnL'] = positions_df['value'] - positions_df['Yvalue']

        # Handle conversion of 'm2m' column to int if it exists
        if "m2m" in positions_df.columns:
            try:
                positions_df['m2m'] = positions_df['m2m'].astype(int)
            except ValueError:
                # Handle the case where some values cannot be converted to int
                pass

        return positions_df

    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()
        return None
