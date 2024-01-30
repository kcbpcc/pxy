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
from nrmlbukdpxy import sum_last_numerical_value_in_each_row_nrml
###########################################################################################################################################################################################################
file_path = 'filePnL.csv'
result = sum_last_numerical_value_in_each_row(file_path)  
file_path_nrml = "filePnL_nrml.csv"
result_nrml = sum_last_numerical_value_in_each_row_nrml(file_path_nrml)
###########################################################################################################################################################################################################
SILVER = "\033[97m"
UNDERLINE = "\033[4m"
RED = "\033[91m"
GREEN = "\033[92m"
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
                        columns_to_drop = ['smb_power', 'oPL%', 'pstp', '_pstp', 'qty', 'close', 'open', 'high', 'low', 'PL%_H', 'dPL%', 'pxy','yxp']
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
def nrml_order_place(index, row):
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
                product='NRML',
                variety='regular',
                price=round_to_paise(row['ltp'], -0.3)
            )
            if order_id:
                logging.info(f"Order {order_id} placed for {exchsym[1]} successfully")                                
                # Write the row to the CSV file here
                with open(csv_file_path_nrml, 'a', newline='') as csvfile:
                    csvwriter = csv.writer(csvfile)
                    csvwriter.writerow(row.tolist())  # Write the selected row to the CSV file
                    try:
                        import telegram
                        import asyncio
                        columns_to_drop = ['smb_power', 'oPL%', 'pstp', '_pstp', 'qty', 'close', 'open', 'high', 'low', 'PL%_H', 'dPL%', 'pxy','yxp']
                        # Dropping specified columns from the row
                        for column in columns_to_drop:
                            if column in row:
                                del row[column]
                        message_text = f"{str(row):>10} \nhttps://console.zerodha.com/verified/f5f15318\nBooked profit until now: {result_nrml}"
                        # Define the bot token and your Telegram username or ID
                        bot_token = '6396096532:AAG5adz_SeUwV8WLn7miteljk_pRrpt8mO0'  # Replace with your actual bot token
                        user_usernames = ('-4067167377')  # Replace with your Telegram username or ID
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
def nrml_AVARAGE_order_place(index, row):
    try:
        exchsym = str(index).split(":")
        if len(exchsym) >= 2:
            logging.info(f"Placing order for {exchsym[1]}, {str(row)}")
            order_id = broker.order_place(
                tradingsymbol=exchsym[1],
                exchange=exchsym[0],
                transaction_type='BUY',
                quantity=50,
                order_type='MARKET',
                product='NRML',
                variety='regular',
                price=round_to_paise(row['ltp'], -0.3)
            )
            if order_id:
                logging.info(f"Order {order_id} placed for {exchsym[1]} successfully")                                
                # Write the row to the CSV file here
                with open(csv_file_path_nrml, 'a', newline='') as csvfile:
                    csvwriter = csv.writer(csvfile)
                    csvwriter.writerow(row.tolist())  # Write the selected row to the CSV file
                    try:
                        import telegram
                        import asyncio
                        columns_to_drop = ['smb_power', 'oPL%', 'pstp', '_pstp', 'qty', 'close', 'open', 'high', 'low', 'PL%_H', 'dPL%', 'pxy','yxp']
                        # Dropping specified columns from the row
                        for column in columns_to_drop:
                            if column in row:
                                del row[column]
                        message_text = f"{str(row):>10} \nhttps://console.zerodha.com/verified/f5f15318\nBooked profit until now: {result}"
                        # Define the bot token and your Telegram username or ID
                        bot_token = '6396096532:AAG5adz_SeUwV8WLn7miteljk_pRrpt8mO0'  # Replace with your actual bot token
                        user_usernames = ('-4067167377')  # Replace with your Telegram username or ID
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
def order_place_avg(index, row):
    try:
        exchsym = str(index).split(":")
        # Check existing positions
        positions_response = broker.kite.positions()
        open_positions = positions_response.get('net', [])
        existing_position = next((position for position in open_positions if position['tradingsymbol'] == exchsym[1]), None)
        if existing_position:
            logging.info(f"Position already exists for {exchsym[1]}. Skipping order placement.")
            return True
        if len(exchsym) >= 2 :
            logging.info(f"Placing order for {exchsym[1]}, {str(row)}")
            # Calculate quantity based on the value of 5000
            qty = 5000 // row['ltp']
            qty = int(qty)  # Remove decimals
            order_id = broker.order_place(
                tradingsymbol=exchsym[1],
                exchange=exchsym[0],
                transaction_type='BUY',
                quantity=qty,
                order_type='LIMIT',
                product='CNC',
                variety='regular',
                price=round_to_paise(row['ltp'], +0.3)
            )
            if order_id:
                logging.info(f"BUY {order_id} placed for {exchsym[1]} successfully")
                # No need to calculate remaining available cash in this case
                try:
                    message_text = f"{row['ltp']} \nhttps://www.tradingview.com/chart/?symbol={exchsym[1]}"
                    # Define the bot token and your Telegram username or ID
                    bot_token = '6704281753:AAEed33wBCxEN81n-NUfajo8pm9gcCVxeZg'  # Replace with your actual bot token
                    user_id = '-4093430309'  # Replace with your Telegram user ID
                    # Function to send a message to Telegram
                    async def send_telegram_message(message_text):
                        bot = telegram.Bot(token=bot_token)
                        await bot.send_message(chat_id=user_id, text=message_text)
                    # Send the 'row' content as a message to Telegram immediately after printing the row
                    asyncio.run(send_telegram_message(message_text))
                except Exception as e:
                    # Handle the exception (e.g., log it) and continue with your code
                    print(f"Error sending message to Telegram: {e}")
                return exchsym[1], remaining_cash  # Define remaining_cash appropriately
            return True
        else:
            logging.error("Order placement failed")
    except Exception as e:
        # print(traceback.format_exc())
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
    import random
    import os
    import numpy as np
    from mktpxy import get_market_check
    onemincandlesequance, mktpxy = get_market_check()
    import importlib
    from nftpxy import nse_action, nse_power, Day_Change, Open_Change
    import math
    from bukdpxy import sum_last_numerical_value_in_each_row
    from nrmlbukdpxy import sum_last_numerical_value_in_each_row_nrml
    from swchpxy import analyze_stock
    import telegram
    import asyncio
    from selfpxy import get_random_spiritual_message
    from optpxy import get_optpxy
    optpxy = get_optpxy()
    random_message = get_random_spiritual_message()
    switch = analyze_stock()
    #from ordpxy import get_open_order_status
    # Replace 'filePnL.csv' with the path to your actual CSV file
    file_path = 'filePnL.csv'
    result = sum_last_numerical_value_in_each_row(file_path)  
    file_path_nrml = "filePnL_nrml.csv"
    result_nrml = sum_last_numerical_value_in_each_row_nrml(file_path_nrml)
    #from telpxy import send_telegram_message
    #csv_file_path = "filePnL.csv"
    #total_profit_main = process_csv(csv_file_path)
    SILVER = "\033[97m"
    UNDERLINE = "\033[4m"
    RESET = "\033[0m"
    logging.debug("Are we having any holdings to check")
    holdings_response = broker.kite.holdings()
    positions_response = broker.kite.positions()['net']
    holdings_df = get_holdingsinfo(holdings_response, broker)
    positions_df = get_positionsinfo(positions_response, broker)
    ###########################################################################################################################################################################################################
    try:
        response = broker.kite.margins()
        available_cash = response["equity"]["available"]["live_balance"]
        # Rest of your code that depends on the 'available_cash' variable
    except Exception as e:
        print(f"An error occurred: {e}")
        # Handle the error as needed
        # Set available_cash to 0 or any other default value
        available_cash = 0
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
    epsilon = 1e-10
    combined_df[['smb_power']] = combined_df.apply(
    lambda row: pd.Series({
        'smb_power': round(
            abs(row['ltp'] - (row['low'] - 0.01)) / (abs(row['high'] + 0.01) - abs(row['low'] - 0.01) + epsilon)
            if (abs(row['high'] + 0.01) - abs(row['low'] - 0.01) + epsilon != 0) and (row['ltp'] - (row['low'] - 0.01) != 0)
            else 0.5,
            2
        ),
    }), axis=1
    )
    from nftpxy import nse_action, nse_power   
    threshold = 3
###########################################################################################################################################################################################################
    nse_factor = {"Bearish": 0.5, "Bear": 1.0, "Bull": 1.5, "Bullish": 2.0}.get(nse_action, 1.0) 
    options_nse_factor = {"Bearish": 2.0, "Bear": 1.5, "Bull": 0.10, "Bullish": 0.5}.get(nse_action, 1.0)  
    exp_nse_factor = math.exp(options_nse_factor)
    combined_df['otPL%'] = 25 #round(33 * exp_nse_factor, 2) * (1 - ((1+ combined_df['qty'])/500)) 
    combined_df['fPL%'] = combined_df['smb_power'].apply(lambda x: round(np.exp(np.clip(((x + nse_power) / 2), -threshold, threshold)), 2))
    combined_df['tPL%'] = np.round(np.maximum(combined_df['fPL%'], np.maximum(1.4, np.round(np.exp(np.clip(((combined_df['fPL%'] + nse_power) / 2), -threshold, threshold)), 2)) * nse_factor), 2)
###########################################################################################################################################################################################################
    subprocess.run(['python3', 'prftpxy.py'])
    subprocess.run(['python3', 'nrmlprftpxy.py'])
###########################################################################################################################################################################################################
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
    # Round all numeric columns to 2 decimal places
    numeric_columns = ['fPL%','tPL%','smb_power','oPL%','otPL%','_pstp','qty', 'average_price', 'Invested','Yvalue', 'ltp','close', 'open', 'high', 'low','value', 'PnL', 'PL%','PL%_H', 'dPnL', 'dPL%']
    combined_df[numeric_columns] = combined_df[numeric_columns].round(2)        # Filter combined_df
    filtered_df = combined_df[((combined_df['product'] == 'NRML') | ((combined_df['product'].isin(['CNC', 'MIS'])) & (combined_df['qty'] != 0)))]
    # Filter combined_df for rows where 'qty' is greater than 0
    combined_df_positive_qty = combined_df[(combined_df['qty'] > 0) & (combined_df['source'] == 'holdings')]
    # Calculate and print the sum of 'PnL' values and its total 'PL%' for rows where 'qty' is greater than 0
    total_PnL = round(combined_df_positive_qty['PnL'].sum())
    total_PnL_percentage = (total_PnL / combined_df_positive_qty['Invested'].sum()) * 100 if combined_df_positive_qty['Invested'].sum() != 0 else 0   
    # Calculate total_PnL_percentage_nrml_buy
    cnc_buy_df = combined_df.loc[(combined_df['product'] == "CNC") & (combined_df['qty'] > 0) & (combined_df['source'] == "positions")]
    total_PnL_cnc_buy = round(cnc_buy_df['PnL'].sum()) if not cnc_buy_df.empty else 0    
    nrml_buy_df = combined_df.loc[(combined_df['product'] == "NRML")]
    total_PnL_nrml_buy = round(nrml_buy_df['PnL'].sum()) if not nrml_buy_df.empty else 0
    # Calculate and print the sum of 'dPnL' values and its total 'dPL%' for rows where 'qty' is greater than 0
    #total_dPnL = combined_df_positive_qty['dPnL'].sum()
    total_dPnL = round(combined_df_positive_qty['dPnL'].sum())
    total_dPnL_percentage = (total_dPnL / combined_df_positive_qty['Invested'].sum()) * 100 if combined_df_positive_qty['Invested'].sum() != 0 else 0
    total_dPnL = round(combined_df_positive_qty['dPnL'].sum())
###########################################################################################################################################################################################################
    import pandas as pd
    from tabulate import tabulate
    # Define the file path for the CSV file
    lstchk_file = "fileHPdf.csv"
    # Dump the DataFrame to the CSV file, overwriting any existing file
    combined_df.to_csv(lstchk_file, index=False)
    #print(f"DataFrame has been saved to {lstchk_file}")
    # Create a copy of 'filtered_df' and select specific columns
    pxy_df = filtered_df.copy()[['fPL%','tPL%','smb_power','oPL%','otPL%','_pstp','source','product', 'qty','average_price', 'close', 'ltp', 'open', 'high','low','key','dPL%','PnL','PL%_H', 'PL%']]
    pxy_df['avg'] =filtered_df['average_price']
    # Create a copy for just printing 'filtered_df' and select specific columns
    EXE_df = pxy_df[['tPL%','fPL%','smb_power','oPL%','otPL%','_pstp','qty', 'avg', 'close', 'ltp', 'open', 'high', 'low', 'PL%_H', 'dPL%','product', 'source', 'key', 'PL%', 'PnL']]    
    PRINT_df = pxy_df[['source','product','key','fPL%','tPL%','PL%','PnL','qty','smb_power']]
    # Rename columns for display
    PRINT_df = PRINT_df.rename(columns={'source': 'HP', 'product': '_CM', 'qty': 'Q', 'smb_power': 'TR','key': 'key','dPL%': 'dPL%'})
    # Conditionally replace values in the 'HP' column
    PRINT_df['HP'] = PRINT_df['HP'].replace({'holdings': '📌', 'positions': '🎯'})
    # Conditionally replace values in the '_CM' column
    PRINT_df['_CM'] = PRINT_df['_CM'].replace({'CNC': '🧰', 'NRML': '⌛'}) 
    PRINT_df['Q'] = PRINT_df['Q'].apply(lambda Q: '+' if Q > 0 else ('-' if Q < 0 else ''))
    PRINT_df['TR'] = PRINT_df['TR'].apply(lambda TR: 
        '⚪' if TR > 0.8 else (
            '🟢' if 0.5 < TR <= 0.8 else (
                '🟠' if 0.3 < TR <= 0.5 else (
                    '🔴' if TR <= 0.3 else TR
                )
            )
        )
    )
    # Convert the 'PnL' column to integers
    # Remove 'BSE:' or 'NSE:' from the 'key' column
    PRINT_df['key'] = PRINT_df['key'].str.replace(r'BSE:|NSE:', '', regex=True)
    # Sort the DataFrame by 'PL%' in ascending order
    # Assuming you have a DataFrame named PRINT_df
###########################################################################################################################################################################################################    
    import pandas as pd
    # Assuming PRINT_df_sorted is your DataFrame
    PRINT_df_sorted = PRINT_df.copy()
    # Apply the lambda function to limit 'chks' to 2 characters
    PRINT_df_sorted['TR'] = PRINT_df_sorted['TR'].apply(lambda TR: TR[:2] if isinstance(TR, str) else TR)
    # Remove 'BSE:' or 'NSE:' from the 'key' column and limit to 3 characters
    PRINT_df_sorted['key'] = PRINT_df_sorted['key'].str.replace(r'(BSE:|NSE:|NFO:)', '', regex=True).str[:9].str.ljust(9, ' ')
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
    #print("━" * 42)
    # Always print "Table" in bright yellow
    # Print the truncated DataFrame without color
    # Assuming PRINT_df_sorted_display is your DataFrame
    cnc_filtered_df = PRINT_df_sorted_display[(PRINT_df_sorted_display['PL%'] > PRINT_df_sorted_display['fPL%'] ) & (PRINT_df_sorted_display['Q'] == '+') & (PRINT_df_sorted_display['_CM'] == '🧰')]
    nrml_filtered_df = pxy_df.loc[pxy_df['key'].str.startswith('NFO'), ['key','otPL%', 'tPL%', 'PL%', 'PnL', 'qty', 'smb_power']]
    nrml_filtered_df['otPL%'] = nrml_filtered_df['otPL%'].round(2)    
    nrml_filtered_df['key'] = nrml_filtered_df['key'].str.replace('NFO:NIFTY', '')
###########################################################################################################################################################################################################
    if not cnc_filtered_df.empty:
        print("━" * 42)
        print(f"{BRIGHT_YELLOW}HP|CM|STOCK     |fPL%|tPL%|PL% |PL |Q|TR{RESET}")
        print("━" * 42)
        print(cnc_filtered_df.to_string(index=False, justify='left', col_space=-0, header=False))    
###########################################################################################################################################################################################################
    import csv
    
    # Specify the CSV file name
    file_name = 'mempxy.csv'
    
    # Read data from the CSV file
    with open(file_name, 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            auto_value = row['AUTO']
    
    # Now, you can use the 'auto_value' variable in your program
###########################################################################################################################################################################################################   
    from utcpxy import peak_time
    utct = peak_time()
    #print(utct)
    # Define the CSV file path
    csv_file_path = "filePnL.csv"
    csv_file_path_nrml = 'filePnL_nrml.csv'
    # Create an empty list to store the rows that meet the condition
    selected_rows = []
    # Loop through the DataFrame and place orders based on conditions
    if nse_power < 1 :
        try:
            for index, row in EXE_df.iterrows():
                excluded_keys = set(pd.read_csv("filePnL.csv", header=None).iloc[:, -3])
                key = row['key']  # Get the 'key' value
                symbol_in_order = row['key'].split(":")[1]
                # Check the common conditions first
                if (
                    row['key'] not in excluded_keys and
                    row['open'] > 0 and
                    row['high'] > 0 and
                    row['low'] > 0 and
                    row['close'] > 0 and
                    row['ltp'] != 0                   
                ):                            
###########################################################################################################################################################################################################                    
                    if (
                        (row['qty'] > 0 and
                         row['avg'] != 0 and
                         nse_power < 0.9 and
                         row['product'] == 'CNC' and
                         row['PL%'] > 1.4 and
                         row['PL%'] > row['fPL%'] and
                         mktpxy in ['Sell', 'Bear']) and
                        (
                            (row['source'] == 'holdings' and row['PL%'] > row['tPL%']) or (row['source'] == 'positions' and row['PL%'] > row['tPL%'])
                        )
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
                        row['avg'] != 0 and
                        row['product'] == 'NRML' and
                        auto_value == 'AUTO'and
                        optpxy in ['Bull'] and
                        row['PL%'] > row['otPL%']
                    ):
                        try:                            
                            is_placed = nrml_order_place(key, row) if get_open_order_status(symbol_in_order) == "NO" else False
                            if is_placed:
                                # Print the row before placing the order
                                print(row)                                
                        except InputException as e:
                            # Handle the specific exception and print only the error message
                            print(f"An error occurred while placing an order for key {key}: {e}")
                        except Exception as e:
                            # Handle any other exceptions that may occur during order placement
                            print(f"An unexpected error occurred while placing an order for key {key}: {e}")
                            #mktpxy in ['Sell-opts'] and
########################################################################################################################################################################################################### 
                    elif (
                        row['qty'] == 0 and
                        optpxy in ['Bear'] and
                        available_cash > 10000 and
                        auto_value == 'AUTO'and
                        row['product'] == 'NRML'
                    ):
                        try:                            
                            is_placed = nrml_AVARAGE_order_place(key, row) if get_open_order_status(symbol_in_order) == "NO" else False
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
                        (row['qty'] > 0 and
                         row['avg'] != 0 and
                         available_cash > 20000 and
                         nse_power < 0.1 and
                         mktpxy in ['Buy', 'Bull'] and
                         row['PL%'] < -14)
                    ):
                        try:                            
                            is_placed = order_place_avg(key, row) if get_open_order_status(symbol_in_order) == "NO" else False
                            if is_placed:
                                # Print the row before placing the order
                                print(row['key'])                                
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
    from dshpxy import get_holdingsinfo
    red_Stocks_count, green_Stocks_count, all_Stocks_capital_lacks, all_Stocks_worth_lacks, zero_qty_count, green_Stocks_profit_loss, green_Stocks_capital_rercentage = get_holdingsinfo('fileHPdf.csv')    
    from bordpxy import printbord
    printbord(Day_Change, result, total_PnL_percentage, total_dPnL, total_PnL, total_dPnL_percentage,
             result_nrml, total_PnL_cnc_buy, total_PnL_nrml_buy, available_cash, auto_value,
             nse_action, nse_power,red_Stocks_count,green_Stocks_count,all_Stocks_capital_lacks,all_Stocks_worth_lacks, zero_qty_count, green_Stocks_profit_loss, green_Stocks_capital_rercentage, mktpxy)
###########################################################################################################################################################################################################
    formatted_lines = nrml_filtered_df[['key', 'qty', 'otPL%', 'PL%', 'PnL']].to_string(index=False, header=False).split('\n')
    
    # Iterate over each line and format it with color based on PnL value
    for line in formatted_lines:
        values = line.split()
        pnl_value = float(values[-1])
        
        # Set color based on PnL value
        if pnl_value > 0:
            color_code = GREEN  # Using GREEN for green text
        else:
            color_code = RED  # Using RED for red text
        
        # Print the formatted line with the selected color and reset color after the line
        print(color_code + ' '.join(values) + RESET)
    print("━" * 42)        
###########################################################################################################################################################################################################
except Exception as e:
    remove_token(dir_path)
    print(traceback.format_exc())
    logging.error(f"{str(e)} in the main loop")
