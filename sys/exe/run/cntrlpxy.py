print(f'🏛🏛 PXY® PreciseXceleratedYield Pvt Ltd™ 🏛🏛')
from toolkit.logger import Logger
from toolkit.currency import round_to_paise
from login_get_kite import get_kite, remove_token
import sys
from time import sleep
import traceback
import os
import subprocess
from cnstpxy import dir_path
from colorama import Fore, Style
import csv
import telegram
import asyncio
from bukdpxy import sum_last_numerical_value_in_each_row

###########################################################################################################################################################################################################
file_path = 'filePnL.csv'
result = sum_last_numerical_value_in_each_row(file_path)  
###########################################################################################################################################################################################################

SILVER = "\033[97m"
UNDERLINE = "\033[4m"
RESET = "\033[0m"
logging = Logger(30, dir_path + "main.log")

try:
    sys.stdout = open('output.txt', 'w')
    broker = get_kite(api="bypass", sec_dir=dir_path)
except Exception as e:
    remove_token(dir_path)
    print(traceback.format_exc())
    logging.error(f"{str(e)} unable to get holdings")
    sys.exit(1)


file_path = 'filePnL.csv'

###########################################################################################################################################################################################################

def get_open_order_status(symbol):
    try:
        orders = broker.kite.orders()

        for order in orders:
            if order['status'] == 'OPEN' and order['tradingsymbol'] == symbol:
                return "YES"  # There is at least one open order for the symbol

    except Exception as e:
        remove_token(dir_path)
        logging.error(f"{str(e)} unable to get orders")
        sys.exit(1)

    return "NO"  # No open orders found for the symbol

###########################################################################################################################################################################################################
def order_place(index, row):
    try:
        exchsym = str(index).split(":")
        if len(exchsym) >= 2:
            logging.info(f"Placing order for {exchsym[1]}, {str(row)}")
            order_id = broker.order_place(
                tradingsymbol=exchsym[1],
                exchange=exchsym[0],
                transaction_type='SELL',
                quantity=int(row['qty']),
                order_type='LIMIT',
                product='CNC',
                variety='regular',
                price=round_to_paise(row['ltp'], -0.3)
            )
            if order_id:
                logging.info(f"Order {order_id} placed for {exchsym[1]} successfully")                                
                # Write the row to the CSV file here
                with open(csv_file_path, 'a', newline='') as csvfile:
                    csvwriter = csv.writer(csvfile)
                    csvwriter.writerow(row.tolist())  # Write the selected row to the CSV file
                    try:
                        import telegram
                        import asyncio
                    
                        columns_to_drop = ['smbchk', 'oPL%', 'pstp', '_pstp', 'qty', 'close', 'open', 'high', 'low', 'PL%_H', 'dPL%', 'pxy','yxp']
                    
                        # Dropping specified columns from the row
                        for column in columns_to_drop:
                            if column in row:
                                del row[column]
                    
                        message_text = f"{str(row):>10} \nhttps://www.tradingview.com/chart/?symbol={key}\nBooked profit until now: {result}"
                        
                        # Define the bot token and your Telegram username or ID
                        bot_token = '6409002088:AAH9mu0lfjvHl_IgRAgX7YrjJQa2Ew9qaLo'  # Replace with your actual bot token
                        user_usernames = ('-4022487175')  # Replace with your Telegram username or ID
                        
                        # Function to send a message to Telegram
                        async def send_telegram_message(message_text):
                            bot = telegram.Bot(token=bot_token)
                            await bot.send_message(chat_id=user_usernames, text=message_text)
                    
                    except Exception as e:
                        # Handle the exception (e.g., log it) and continue with your code
                        print(f"Error sending message to Telegram: {e}")
                    
                    # Send the 'row' content as a message to Telegram immediately after printing the row
                    loop = asyncio.get_event_loop()
                    loop.run_until_complete(send_telegram_message(message_text))
                
                return True                
            else:
                logging.error("Order placement failed")       
        else:
            logging.error("Invalid format for 'index'")    
    except Exception as e:
        #print(traceback.format_exc())
        logging.error(f"{str(e)} while placing order")
    return False
###########################################################################################################################################################################################################
def mis_order_sell(index, row):
    try:
        exchsym = str(index).split(":")
        if len(exchsym) >= 2:
            logging.info(f"Placing order for {exchsym[1]}, {str(row)}")
            order_id = broker.order_place(
                tradingsymbol=exchsym[1],
                exchange=exchsym[0],
                transaction_type='SELL',
                quantity=int(row['qty']),
                order_type='MARKET',
                product='MIS',
                variety='regular',
                price=round_to_paise(row['ltp'], -0.3)
            )
            if order_id:
                logging.info(f"Order {order_id} placed for {exchsym[1]} successfully")                                
                # Write the row to the CSV file here
                with open(csv_file_path, 'a', newline='') as csvfile:
                    csvwriter = csv.writer(csvfile)
                    csvwriter.writerow(row.tolist())  # Write the selected row to the CSV file
                    try:
                        import telegram
                        import asyncio
                    
                        columns_to_drop = ['smbchk', 'oPL%', 'pstp', '_pstp', 'qty', 'close', 'open', 'high', 'low', 'PL%_H', 'dPL%', 'pxy','yxp']
                    
                        # Dropping specified columns from the row
                        for column in columns_to_drop:
                            if column in row:
                                del row[column]
                    
                        message_text = f"{str(row):>10} \nhttps://www.tradingview.com/chart/?symbol={key}\nBooked profit until now: {result}"
                        
                        # Define the bot token and your Telegram username or ID
                        bot_token = '6409002088:AAH9mu0lfjvHl_IgRAgX7YrjJQa2Ew9qaLo'  # Replace with your actual bot token
                        user_usernames = ('-4022487175')  # Replace with your Telegram username or ID
                        
                        # Function to send a message to Telegram
                        async def send_telegram_message(message_text):
                            bot = telegram.Bot(token=bot_token)
                            await bot.send_message(chat_id=user_usernames, text=message_text)
                    
                    except Exception as e:
                        # Handle the exception (e.g., log it) and continue with your code
                        print(f"Error sending message to Telegram: {e}")
                    
                    # Send the 'row' content as a message to Telegram immediately after printing the row
                    loop = asyncio.get_event_loop()
                    loop.run_until_complete(send_telegram_message(message_text))
                
                return True                
            else:
                logging.error("Order placement failed")       
        else:
            logging.error("Invalid format for 'index'")    
    except Exception as e:
        #print(traceback.format_exc())
        logging.error(f"{str(e)} while placing order")
    return False
###########################################################################################################################################################################################################
def mis_order_buy(index, row):
    try:
        exchsym = str(index).split(":")
        if len(exchsym) >= 2:
            logging.info(f"Placing order for {exchsym[1]}, {str(row)}")
            order_id = broker.order_place(
                tradingsymbol=exchsym[1],
                exchange=exchsym[0],
                transaction_type='BUY',
                quantity=int(-1*row['qty']),
                order_type='MARKET',
                product='MIS',
                variety='regular',
                price=round_to_paise(row['ltp'], +0.3)
            )
            if order_id:
                logging.info(f"Order {order_id} placed for {exchsym[1]} successfully")                                
                # Write the row to the CSV file here
                with open(csv_file_path, 'a', newline='') as csvfile:
                    csvwriter = csv.writer(csvfile)
                    csvwriter.writerow(row.tolist())  # Write the selected row to the CSV file
                    try:
                        import telegram
                        import asyncio
                    
                        columns_to_drop = ['smbchk', 'oPL%', 'pstp', '_pstp', 'qty', 'close', 'open', 'high', 'low', 'PL%_H', 'dPL%', 'pxy','yxp']
                    
                        # Dropping specified columns from the row
                        for column in columns_to_drop:
                            if column in row:
                                del row[column]
                    
                        message_text = f"{str(row):>10} \nhttps://www.tradingview.com/chart/?symbol={key}\nBooked profit until now: {result}"
                        
                        # Define the bot token and your Telegram username or ID
                        bot_token = '6409002088:AAH9mu0lfjvHl_IgRAgX7YrjJQa2Ew9qaLo'  # Replace with your actual bot token
                        user_usernames = ('-4022487175')  # Replace with your Telegram username or ID
                        
                        # Function to send a message to Telegram
                        async def send_telegram_message(message_text):
                            bot = telegram.Bot(token=bot_token)
                            await bot.send_message(chat_id=user_usernames, text=message_text)
                    
                    except Exception as e:
                        # Handle the exception (e.g., log it) and continue with your code
                        print(f"Error sending message to Telegram: {e}")
                    
                    # Send the 'row' content as a message to Telegram immediately after printing the row
                    loop = asyncio.get_event_loop()
                    loop.run_until_complete(send_telegram_message(message_text))
                
                return True                
            else:
                logging.error("Order placement failed")       
        else:
            logging.error("Invalid format for 'index'")    
    except Exception as e:
        #print(traceback.format_exc())
        logging.error(f"{str(e)} while placing order")
    return False

###########################################################################################################################################################################################################
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
###########################################################################################################################################################################################################
try:
    import sys
    import traceback
    import pandas as pd
    import datetime
    import time
    from login_get_kite import get_kite, remove_token
    from cnstpxy import dir_path
    from toolkit.logger import Logger
    from toolkit.currency import round_to_paise
    import csv
    from cnstpxy import sellbuff, secs, perc_col_name
    from time import sleep
    import subprocess
    #from prftpxy import process_csv
    import random
    import os
    import numpy as np
    from mktpxy import get_market_check
    import importlib
    from nftpxy import nse_action, nse_power
    from timepxy import calculate_timpxy
    import math
    from bukdpxy import sum_last_numerical_value_in_each_row
    from swchpxy import analyze_stock
    import telegram
    import asyncio
    from smbpxy import get_smbpxy_check
    #from ordpxy import get_open_order_status
    yellow_color_code = "\033[93m"  # Replace with your actual ANSI color code for yellow
    reset_color_code = "\033[0m"    # Replace with your actual ANSI color code for resetting color
    print(f"{yellow_color_code}Market is {nse_action}⚡💥 -- Power⚡💥{nse_power}{reset_color_code}💥⚡")
    # Replace 'filePnL.csv' with the path to your actual CSV file
    file_path = 'filePnL.csv'
    result = sum_last_numerical_value_in_each_row(file_path)  
    #from telpxy import send_telegram_message
    timpxy = calculate_timpxy()
    #csv_file_path = "filePnL.csv"
    #total_profit_main = process_csv(csv_file_path)
    mktpxy = get_market_check('^NSEI')
    SILVER = "\033[97m"
    UNDERLINE = "\033[4m"
    RESET = "\033[0m"
    logging.debug("Are we having any holdings to check")
    holdings_response = broker.kite.holdings()
    positions_response = broker.kite.positions()['net']
    holdings_df = get_holdingsinfo(holdings_response, broker)
    positions_df = get_positionsinfo(positions_response, broker)
    ###########################################################################################################################################################################################################
 
    response = broker.kite.margins()
    available_cash = response["equity"]["available"]["live_balance"]  
    # Add 'key' column to holdings_df and positions_df
    # Create 'key' column if holdings_df is not empty
    holdings_df['key'] = holdings_df['exchange'] + ":" + holdings_df['tradingsymbol'] if not holdings_df.empty else None
    # Create 'key' column if positions_df is not empty
    positions_df['key'] = positions_df['exchange'] + ":" + positions_df['tradingsymbol'] if not positions_df.empty else None
    combined_df = pd.concat([holdings_df, positions_df], ignore_index=True)
    # Get OHLC data for the 'key' column
    lst = combined_df['key'].tolist()
    resp = broker.kite.ohlc(lst)
    # Create a dictionary from the response for easier mapping
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
    # Add 'ltp', 'open', 'high', and 'low' columns to the DataFrame
    combined_df['ltp'] = combined_df.apply(lambda row: dct.get(row['key'], {}).get('ltp', row['last_price']), axis=1)
    combined_df['open'] = combined_df['key'].map(lambda x: dct.get(x, {}).get('open', 0))
    combined_df['high'] = combined_df['key'].map(lambda x: dct.get(x, {}).get('high', 0))
    combined_df['low'] = combined_df['key'].map(lambda x: dct.get(x, {}).get('low', 0))
    combined_df['close'] = combined_df['key'].map(lambda x: dct.get(x, {}).get('close_price', 0))
    combined_df['qty'] = combined_df.apply(lambda row: int(row['quantity'] + row['t1_quantity']) if row['source'] == 'holdings' else int(row['quantity']), axis=1)
    combined_df['oPL%'] = combined_df.apply(lambda row: (((row['ltp'] - row['open']) / row['open']) * 100) if row['open'] != 0 else 1, axis=1)
    combined_df['pstp'] = (combined_df['average_price'] *0.99)
    combined_df['_pstp'] = (combined_df['average_price'] *1.01) 
###########################################################################################################################################################################################################
    subprocess.run(['python3', 'cpritepxy.py'])
    subprocess.run(['python3', 'dshpxy.py'])
    subprocess.run(['python3', 'prftpxy.py'])
    print(f'{SILVER}{UNDERLINE}🏛🏛 PXY® PreciseXceleratedYield Pvt Ltd™ 🏛🏛{RESET}')
###########################################################################################################################################################################################################
    smb500_list = pd.read_csv('smb500.csv')['tradingsymbol'].tolist()
    combined_df['smbchk'] = combined_df.apply(lambda row: get_smbpxy_check(row['tradingsymbol'] + ".NS") if row['qty'] != 0 and row['tradingsymbol'] in smb500_list and get_smbpxy_check(row['tradingsymbol'] + ".NS") is not None else mktpxy, axis=1)
    # Calculate 'Invested' column
    combined_df['Invested'] = combined_df['qty'] * combined_df['average_price']
    # Calculate 'value' column as 'qty' * 'ltp'
    combined_df['value'] = combined_df['qty'] * combined_df['ltp']
    combined_df['value_H'] = combined_df['qty'] * combined_df['high']
    # Calculate 'PnL' column as 'value' - 'Invested'
    combined_df['PnL'] = (combined_df['value'] - combined_df['Invested']).astype(int)
    combined_df['PnL_H'] = combined_df['value_H'] - combined_df['Invested']
    # Calculate 'PL%' column as ('PnL' / 'Invested') * 100
    combined_df['PL%'] = ((combined_df['PnL'] / combined_df['Invested']) * 100).round(2)
    #combined_df['PL%'] = ((combined_df['PnL'] / combined_df['Invested']) * 100) * np.where(combined_df['qty'] < 0, -1, 1)
    combined_df['PL%_H'] = (combined_df['PnL_H'] / combined_df['Invested']) * 100
    #combined_df['PL%_H'] = ((combined_df['PnL_H'] / combined_df['Invested']) * 100) * np.where(combined_df['qty'] < 0, -1, 1)
    # Calculate 'Yvalue' column as 'qty' * 'close'
    combined_df['Yvalue'] = combined_df['qty'] * combined_df['close']
    # Calculate 'dPnL' column as 'close_price' - 'ltp'
    combined_df['dPnL'] = combined_df['value'] - combined_df['Yvalue']
    # Calculate 'dPL%' column as ('dPnL' / 'Invested') * 100
    combined_df['dPL%'] = (combined_df['dPnL'] / combined_df['Yvalue']) * 100

###########################################################################################################################################################################################################
    epsilon = 1e-10
    
    combined_df[['strength', 'weakness']] = combined_df.apply(
        lambda row: pd.Series({
            'strength': round((row['ltp'] - (row['low'] - 0.01)) / (abs(row['high'] + 0.01) - abs(row['low'] - 0.01) + epsilon) if (abs(row['high'] + 0.01) - abs(row['low'] - 0.01) + epsilon != 0) and (row['ltp'] - (row['low'] - 0.01) != 0) else 0.5, 2),
            'weakness': round((row['ltp'] - (row['high'] + 0.01)) / (abs(row['high'] + 0.01) - abs(row['low'] - 0.01) + epsilon) if (abs(row['high'] + 0.01) - abs(row['low'] - 0.01) + epsilon != 0) and (row['ltp'] - (row['high'] + 0.01) != 0) else 0.5, 2)
        }), axis=1
    )
    
    combined_df[['pr', 'xl', 'yi', '_pr', '_xl', '_yi']] = combined_df.apply(
        lambda row: pd.Series({
            'pr': round(max(0.5, round(0.0 + (row['strength'] * 1.0), 2) * 1 - epsilon), 2),
            'xl': round(max(1, round(0.0 + (row['strength'] * 1.0), 2) * 2 - epsilon), 2),
            'yi': round(max(1.5, round(0.0 + (row['strength'] * 1.0), 2) * 3 - epsilon), 2),
            '_pr': round(min(-0.5, round(0.0 + (row['weakness'] * 1.0), 2) * 1 - epsilon), 2),
            '_xl': round(min(-1, round(0.0 + (row['weakness'] * 1.0), 2) * 2 - epsilon), 2),
            '_yi': round(min(-1.5, round(0.0 + (row['weakness'] * 1.0), 2) * 3 - epsilon), 2),
        }), axis=1
    )
    
    def calculate_pxy(row):
        smbchk = row['smbchk']
        pr, xl, yi = row['pr'], row['xl'], row['yi']
    
        if smbchk == "Bear": 
            return round(max(pr, pr), 2)
            
        elif smbchk == "Buy": 
            return round(max(pr, yi), 2)

        elif smbchk == "Bull":
            return round(max(pr, yi), 2)

        elif smbchk == "Sell":
            return round(max(pr, xl), 2)
        
        else:
            return round(pr, 2)
    
    def calculate_yxp(row):
        smbchk = row['smbchk']
        _pr, _xl, _yi = row['_pr'], row['_xl'], row['_yi']
    
        if smbchk == "Bear":
            return round(min(_pr, _yi), 2)
    
        elif smbchk == "Buy":
            return round(min(_pr, _xl), 2)
    
        elif smbchk == "Bull":
            return round(min(_pr, _pr), 2)
    
        elif smbchk == "Sell":
            return round(min(_pr, _yi), 2)
    
        else:
            return round(_pr, 2)

    
    combined_df['pxy'] = combined_df.apply(calculate_pxy, axis=1)
    combined_df['yxp'] = combined_df.apply(calculate_yxp, axis=1)
  
###########################################################################################################################################################################################################
    TIMPXY = (
        float(timpxy)
        if (nse_action in ("Bullish"))
        else (
            float(timpxy) * 0.90
            if (nse_action in ("Bull"))
            else (
                float(timpxy) * 0.60
                if (nse_action in ("Bear"))
                else (
                    float(timpxy) * 0.30
                    if (nse_action in ("Bearish"))
                    else 0.50  # You might want to add a default value here
                )
            )
        )
    )

###########################################################################################################################################################################################################    
    # Round all numeric columns to 2 decimal places
    numeric_columns = ['smbchk','oPL%','pstp','_pstp','qty', 'average_price', 'Invested','Yvalue', 'ltp','close', 'open', 'high', 'low','value', 'PnL', 'PL%','PL%_H', 'dPnL', 'dPL%']
    combined_df[numeric_columns] = combined_df[numeric_columns].round(2)        # Filter combined_df
    filtered_df = combined_df[(combined_df['qty'] > 0) | ((combined_df['qty'] < 0) & (combined_df['product'] == 'MIS'))]
    # Filter combined_df for rows where 'qty' is greater than 0
    combined_df_positive_qty = combined_df[(combined_df['qty'] > 0) & (combined_df['source'] == 'holdings')]
    # Calculate and print the sum of 'PnL' values and its total 'PL%' for rows where 'qty' is greater than 0
    total_PnL = round(combined_df_positive_qty['PnL'].sum())
    total_PnL_percentage = (total_PnL / combined_df_positive_qty['Invested'].sum()) * 100 if combined_df_positive_qty['Invested'].sum() != 0 else 0   
    # Calculate total_PnL_percentage_mis_buy
    cnc_buy_df = combined_df.loc[(combined_df['product'] == "CNC") & (combined_df['qty'] > 0) & (combined_df['source'] == "positions")]
    total_PnL_cnc_buy = round(cnc_buy_df['PnL'].sum()) if not cnc_buy_df.empty else 0    
    mis_buy_df = combined_df.loc[(combined_df['product'] == "MIS") & (combined_df['qty'] > 0) & (combined_df['source'] == "positions")]
    total_PnL_mis_buy = round(mis_buy_df['PnL'].sum()) if not mis_buy_df.empty else 0
    # Calculate total_PnL_percentage_mis_sell
    mis_sell_df = combined_df.loc[(combined_df['product'] == "MIS") & (combined_df['qty'] < 0)]
    total_PnL_percentage_mis_sell = round(mis_sell_df['PnL'].sum()) if not mis_sell_df.empty else 0    
    # Calculate and print the sum of 'dPnL' values and its total 'dPL%' for rows where 'qty' is greater than 0
    #total_dPnL = combined_df_positive_qty['dPnL'].sum()
    total_dPnL = round(combined_df_positive_qty['dPnL'].sum())
    total_dPnL_percentage = (total_dPnL / combined_df_positive_qty['Invested'].sum()) * 100 if combined_df_positive_qty['Invested'].sum() != 0 else 0
###########################################################################################################################################################################################################    
    import pandas as pd
    # Assuming you have a list of instrument keys, e.g., ['NIFTY50', 'RELIANCE', ...]
    instrument_keys = ['NSE:NIFTY 50']
    # Create an empty DataFrame named NIFTY
    NIFTY = pd.DataFrame()
    # Get OHLC data for the list of keys
    resp = broker.kite.ohlc("NSE:NIFTY 50")
    # Create a dictionary from the response for easier mapping
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
    # Set the 'key' column to the instrument keys from your list
    NIFTY['key'] = instrument_keys
    # Populate other columns based on the dct dictionary
    NIFTY['ltp'] = NIFTY['key'].map(lambda x: dct.get(x, {}).get('ltp', 0))
    NIFTY['timestamp'] = pd.to_datetime('now').strftime('%H:%M:%S')
    NIFTY['open'] = NIFTY['key'].map(lambda x: dct.get(x, {}).get('open', 0))
    NIFTY['high'] = NIFTY['key'].map(lambda x: dct.get(x, {}).get('high', 0))
    NIFTY['low'] = NIFTY['key'].map(lambda x: dct.get(x, {}).get('low', 0))
    NIFTY['close_price'] = NIFTY['key'].map(lambda x: dct.get(x, {}).get('close_price', 0))
    NIFTY['Day_Change_%'] = round(((NIFTY['ltp'] - NIFTY['close_price']) / NIFTY['close_price']) * 100, 2)
    NIFTY['Open_Change_%'] = round(((NIFTY['ltp'] - NIFTY['open']) / NIFTY['open']) * 100, 2)
    NIFTYconditions = [
        (NIFTY['Day_Change_%'] > 0) & (NIFTY['Open_Change_%'] > 0),
        (NIFTY['Open_Change_%'] > 0) & (NIFTY['Day_Change_%'] < 0),
        (NIFTY['Day_Change_%'] < 0) & (NIFTY['Open_Change_%'] < 0),
        (NIFTY['Day_Change_%'] > 0) & (NIFTY['Open_Change_%'] < 0)
    ]
    choices = ['SuperBull', 'Bull', 'SuperBear', 'Bear']
    NIFTY['Day Status'] = np.select(NIFTYconditions, choices, default='Bear')
    status_factors = {
        'SuperBull': +1,
        'Bull': 0,
        'Bear': 0,
        'SuperBear': -1
    }
    # Calculate 'Score' for each row based on 'Day Status' and 'status_factors'
    NIFTY['Score'] = NIFTY['Day Status'].map(status_factors).fillna(0)
    score_value = NIFTY['Score'].values[0]
    # Assuming you have a DataFrame named "NIFTY" with columns 'ltp', 'low', 'high', 'close'
    # Calculate the metrics
    
    epsilon = 1e-10
    NIFTY['strength']= ((NIFTY['ltp'] - (NIFTY['low'] - 0.01)) / (abs(NIFTY['high'] + 0.01) - abs(NIFTY['low'] - 0.01)))    
    NIFTY['weakness'] = ((NIFTY['ltp'] - (NIFTY['high'] - 0.01)) / (abs(NIFTY['high'] + 0.01) - abs(NIFTY['low'] - 0.01)))
    power = NIFTY['strength'].astype(float).round(2).values[0]

    switch = analyze_stock('^NSEI')
    
###########################################################################################################################################################################################################

    # Define the file path for the CSV file
    lstchk_file = "fileHPdf.csv"
    # Dump the DataFrame to the CSV file, overwriting any existing file
    combined_df.to_csv(lstchk_file, index=False)
    #print(f"DataFrame has been saved to {lstchk_file}")
    # Create a copy of 'filtered_df' and select specific columns
    pxy_df = filtered_df.copy()[['smbchk','oPL%','pstp','_pstp','source','product', 'qty','average_price', 'close', 'ltp', 'open', 'high','low','pxy','yxp','key','dPL%','PnL','PL%_H', 'PL%']]
  
    pxy_df['avg'] =filtered_df['average_price']
    # Create a copy for just printing 'filtered_df' and select specific columns
    EXE_df = pxy_df[['smbchk','oPL%','pstp','_pstp','qty', 'avg', 'close', 'ltp', 'open', 'high', 'low', 'PL%_H', 'dPL%', 'pxy','yxp','product', 'source', 'key', 'PL%', 'PnL']]

    PRINT_df = pxy_df[['source','product','key','yxp','pxy','dPL%','oPL%','PL%','qty','smbchk']]
    # Rename columns for display
    PRINT_df = PRINT_df.rename(columns={'source': 'X', 'product': 'Y', 'qty': 'Q', 'smbchk': 'TR'})
    # Conditionally replace values in the 'HP' column
    PRINT_df['X'] = PRINT_df['X'].replace({'holdings': 'H', 'positions': 'P'})
    # Conditionally replace values in the 'CM' column
    PRINT_df['Y'] = PRINT_df['Y'].replace({'CNC': 'C', 'MIS': 'M'})
    PRINT_df['Q'] = PRINT_df['Q'].apply(lambda Q: f"{'+' if Q > 0 else '-'}")
    PRINT_df['TR'] = PRINT_df['TR'].apply(lambda TR: '🟢' if TR == 'Bull' else ('🔴' if TR == 'Bear' else ('🌚' if TR == 'Sell' else ('🌕' if TR == 'Buy' else TR))))
    # Convert the 'PnL' column to integers
    # Remove 'BSE:' or 'NSE:' from the 'key' column
    PRINT_df['key'] = PRINT_df['key'].str.replace(r'(BSE:|NSE:)', '', regex=True)    
    # Sort the DataFrame by 'PL%' in ascending order
    # Assuming you have a DataFrame named PRINT_df

###########################################################################################################################################################################################################    
    import pandas as pd
    
    # Assuming PRINT_df_sorted is your DataFrame
    PRINT_df_sorted = PRINT_df.copy()
    
    # Apply the lambda function to limit 'chks' to 2 characters
    PRINT_df_sorted['TR'] = PRINT_df_sorted['TR'].apply(lambda TR: TR[:2] if isinstance(TR, str) else TR)
    
    # Remove 'BSE:' or 'NSE:' from the 'key' column and limit to 3 characters
    PRINT_df_sorted['key'] = PRINT_df_sorted['key'].str.replace(r'(BSE:|NSE:)', '', regex=True).str[:3]
    
    # Sort the DataFrame by 'PL%' in ascending order
    PRINT_df_sorted = PRINT_df_sorted.sort_values(by='PL%', ascending=True)
    
    # Convert the 'PL%' column to integers
    #PRINT_df_sorted.loc[:, 'PL%'] = PRINT_df_sorted['PL%'].astype(int)
    
    # ANSI escape codes for text coloring
    RESET = "\033[0m"
    BRIGHT_YELLOW = "\033[93m"
    
    # Set the maximum width for all columns
    pd.set_option('display.max_colwidth', 1)  # Adjust the value for your desired width
    
    # Apply truncation to each cell in the DataFrame
    PRINT_df_sorted_display = PRINT_df_sorted.copy()
    print("*" * 42)
    
    # Always print "Table" in bright yellow
    print(f"{BRIGHT_YELLOW}Table–Stocks above @Pr and might reach @Yi{RESET}")

    # Print the truncated DataFrame without color
    print(PRINT_df_sorted_display.to_string(index=False, justify='left', col_space=-2))
    print("*" * 42)
    print(f"PXY® is running on timepxy ⏰⏰⏰{TIMPXY}⏰⏰⏰")
  
###########################################################################################################################################################################################################
    # Define the CSV file path
    csv_file_path = "filePnL.csv"
    # Create an empty list to store the rows that meet the condition
    selected_rows = []
    # Loop through the DataFrame and place orders based on conditions
    if any(item in mktpxy for item in ['Sell', 'Bear', 'Buy', 'Bull', 'None']):  # Check if mktpxy is one of the specified values
        try:
            for index, row in EXE_df.iterrows():
                key = row['key']  # Get the 'key' value
                symbol_in_order = row['key'].split(":")[1]
                # Check the common conditions first
                if (
                    row['open'] > 0 and
                    row['high'] > 0 and
                    row['low'] > 0 and
                    row['close'] > 0 and
                    row['qty'] != 0
                    
                ):
                            
###########################################################################################################################################################################################################                    
                    if (
                        (row['qty'] > 0 and
                         row['product'] == 'CNC') and
                        (row['ltp'] < (row['high'] * 0.99))
                    ):
                        try:                            
                            is_placed = order_place(key, row) if get_open_order_status(symbol_in_order) == "NO" else False
                            if is_placed:
                                # Print the row before placing the order
                                print(row)                                
                        except InputException as e:
                            # Handle the specific exception and print only the error message
                            print(f"An error occurred while placing an order for key {key}: {e}")
                        except Exception as e:
                            # Handle any other exceptions that may occur during order placement
                            print(f"An unexpected error occurred while placing an order for key {key}: {e}")

###########################################################################################################################################################################################################
                    elif (
                        row['qty'] > 0 and
                        row['product'] == 'MIS' and
                        ((row['PL%'] < -1) or ((row['PL%'] > 0) and (row['PL%'] > row['pxy']))) 
                    ):

                        try:
                            is_placed = mis_order_sell(key, row) if get_open_order_status(symbol_in_order) == "NO" else False
                            if is_placed:
                                # Print the row before placing the order
                                print(row)                                

                        except InputException as e:
                            # Handle the specific exception and print only the error message
                            print(f"An error occurred while placing an order for key {key}: {e}")
                        except Exception as e:
                            # Handle any other exceptions that may occur during order placement
                            print(f"An unexpected error occurred while placing an order for key {key}: {e}")
###########################################################################################################################################################################################################
                    elif (
                        row['qty'] < 0 and
                        row['product'] == 'MIS' and
                        ((row['PL%'] > 1) or ((row['PL%'] < 0) and (row['PL%'] < row['yxp']))) 
                    ):
                        try:
                            is_placed = mis_order_buy(key, row) if get_open_order_status(symbol_in_order) == "NO" else False
                            if is_placed:
                                # Print the row before placing the order
                                print(row)

                        except InputException as e:
                            # Handle the specific exception and print only the error message
                            print(f"An error occurred while placing an order for key {key}: {e}")
                        except Exception as e:
                            # Handle any other exceptions that may occur during order placement
                            print(f"An unexpected error occurred while placing an order for key {key}: {e}")
       
        except Exception as e:
            # Handle any other exceptions that may occur during the loop
            print(f"An unexpected error occurred: {e}")
###########################################################################################################################################################################################################
        
        print(f"{BRIGHT_YELLOW}📉🔀Trades Overview & Market Dynamics 📈🔄 {RESET}")
        # ANSI escape codes for text coloring
        RESET = "\033[0m"
        BRIGHT_YELLOW = "\033[93m"
        BRIGHT_RED = "\033[91m"
        BRIGHT_GREEN = "\033[92m"
        # Print all three sets of values in a single line with rounding to 2 decimal places
        column_width = 30
        left_aligned_format = "{:<" + str(column_width) + "}"
        right_aligned_format = "{:>" + str(column_width) + "}"
        
        # Print statements
        
        print(left_aligned_format.format(f"Status:{BRIGHT_GREEN if nse_action in ('Bullish', 'Bull') else BRIGHT_RED}{nse_action}{RESET}"), end="")
        print(right_aligned_format.format(f"Power:{BRIGHT_GREEN if power > 0.5 else BRIGHT_RED}{power}{RESET}"))
        print(left_aligned_format.format(f"tPL%:{BRIGHT_GREEN if total_PnL_percentage >= 0 else BRIGHT_RED}{round(total_PnL_percentage, 2)}{RESET}"), end="")
        print(right_aligned_format.format(f"dPnL:{BRIGHT_GREEN if total_dPnL > 0 else BRIGHT_RED}{round(total_dPnL, 2)}{RESET}"))
        print(left_aligned_format.format(f"tPnL:{BRIGHT_GREEN if total_PnL >= 0 else BRIGHT_RED}{round(total_PnL, 2)}{RESET}"), end="")
        print(right_aligned_format.format(f"dPL%:{BRIGHT_GREEN if total_dPnL_percentage > 0 else BRIGHT_RED}{round(total_dPnL_percentage, 2)}{RESET}"))
        print(left_aligned_format.format(f"MIS:{BRIGHT_GREEN if total_PnL_percentage_mis_sell >= 0 else BRIGHT_RED}{total_PnL_percentage_mis_sell}{RESET}"), end="")
        print(right_aligned_format.format(f"CNC:{BRIGHT_GREEN if total_PnL_cnc_buy >= 0 else BRIGHT_RED}{total_PnL_cnc_buy}{RESET}"))
        print(left_aligned_format.format(f"Switch:{BRIGHT_YELLOW}{switch}{RESET}"), end="")
        print(right_aligned_format.format(f"Funds:{BRIGHT_GREEN if available_cash > 12000 else BRIGHT_YELLOW}{available_cash:.0f}{RESET}"))
        print(left_aligned_format.format(f"Change%:{BRIGHT_GREEN if NIFTY['Day_Change_%'][0] >= 0 else BRIGHT_RED}{round(NIFTY['Day_Change_%'][0], 2)}{RESET}"), end="")
        print(right_aligned_format.format(f"TIMEPXY:{BRIGHT_GREEN if TIMPXY >= 5 else BRIGHT_RED}{TIMPXY}{RESET}"))
        print(left_aligned_format.format(f"Open%:{BRIGHT_GREEN if NIFTY['Open_Change_%'][0] >= 0 else BRIGHT_RED}{round(NIFTY['Open_Change_%'][0], 2)}{RESET}"), end="")
        print(right_aligned_format.format(f"Booked:{BRIGHT_GREEN if result > 0 else BRIGHT_RED}{round(result)}{RESET}"))

        print("*" * 42)

        print(f'{SILVER}{UNDERLINE}🏛🏛 PXY® PreciseXceleratedYield Pvt Ltd™ 🏛🏛{RESET}')
        mktpxy = get_market_check('^NSEI')
except Exception as e:
    remove_token(dir_path)
    print(traceback.format_exc())
    logging.error(f"{str(e)} in the main loop")
