import sys
import traceback
import pandas as pd
from login_get_kite import get_kite, remove_token
from cnstpxy import dir_path
from toolkit.logger import Logger
import logging

logging = Logger(30, dir_path + "main.log")

def get_holdingsinfo(resp_list, broker):
    try:
        if resp_list:
            df = pd.DataFrame(resp_list)
            df['source'] = 'holdings'
        else:
            df = pd.DataFrame(columns=['exchange', 'tradingsymbol', 'quantity', 't1_quantity', 'average_price', 'pnl'])
        return df
    except Exception as e:
        print(f"An error occurred in holdings: {e}")
        return pd.DataFrame()

def get_positionsinfo(resp_list, broker):
    try:
        if resp_list:
            df = pd.DataFrame(resp_list)
            df['source'] = 'positions'
        else:
            df = pd.DataFrame(columns=['exchange', 'tradingsymbol', 'quantity', 'average_price'])
        return df
    except Exception as e:
        print(f"An error occurred in positions: {e}")
        return pd.DataFrame()

def get_ordersinfo(broker):
    try:
        orders = broker.kite.orders()
        if orders:
            df = pd.DataFrame(orders)
        else:
            df = pd.DataFrame(columns=['order_id', 'tradingsymbol', 'quantity', 'price', 'status'])  # Add other necessary columns
        df.columns = ['o_' + col if col != 'tradingsymbol' else col for col in df.columns]  # Prefix columns with 'o_'
        return df
    except Exception as e:
        print(f"An error occurred in orders: {e}")
        return pd.DataFrame()

try:
    sys.stdout = open('output.txt', 'w')
    broker = get_kite()
except Exception as e:
    remove_token(dir_path)
    print(traceback.format_exc())
    logging.error(f"{str(e)} unable to get holdings")
    sys.exit(1)
finally:
    if sys.stdout != sys.__stdout__:
        sys.stdout.close()
        sys.stdout = sys.__stdout__

def process_data():
    try:
        holdings_response = broker.kite.holdings()
        positions_response = broker.kite.positions()['net']
        orders_df = get_ordersinfo(broker)

        holdings_df = get_holdingsinfo(holdings_response, broker)
        positions_df = get_positionsinfo(positions_response, broker)

        if holdings_df.empty:
            holdings_df = pd.DataFrame(columns=['exchange', 'tradingsymbol', 'quantity', 't1_quantity', 'average_price', 'pnl'])
        else:
            holdings_df['key'] = holdings_df['exchange'] + ":" + holdings_df['tradingsymbol']

        if positions_df.empty:
            positions_df = pd.DataFrame(columns=['exchange', 'tradingsymbol', 'quantity', 'average_price'])
        else:
            positions_df['key'] = positions_df['exchange'] + ":" + positions_df['tradingsymbol']

        combined_df = pd.concat([holdings_df, positions_df], ignore_index=True)

        if not orders_df.empty:
            # Rename columns from orders_df to prefix with 'o_'
            orders_df = orders_df.rename(columns=lambda x: 'o_' + x if x != 'tradingsymbol' else x)
            combined_df = pd.merge(combined_df, orders_df, on='tradingsymbol', how='left')

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

        combined_df['in'] = positions_df['key'].map(holdings_df.set_index('key')['average_price'])
        if positions_df.empty:
            combined_df['in'] = combined_df.get('out', None)
        else:
            combined_df['out'] = positions_df['key'].map(positions_df.set_index('key')['buy_price'])

        if "m2m" in combined_df.columns:
            try:
                combined_df['m2m'] = combined_df['m2m'].astype(int)
            except ValueError:
                pass
        else:
            combined_df['m2m'] = 0

        return combined_df

    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()
        return None
