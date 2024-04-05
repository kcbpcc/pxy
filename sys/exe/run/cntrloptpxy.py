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
from clorpxy import SILVER, UNDERLINE, RED, GREEN, YELLOW, RESET, BRIGHT_YELLOW, BRIGHT_RED, BRIGHT_GREEN, BOLD, GREY
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
    onemincandlesequance, mktpxy = get_market_check('^NSEI')
    from optpxy import get_opt_check
    optpxy = get_opt_check('^NSEI')
    import importlib
    from nftpxy import nse_action, nse_power, Day_Change, Open_Change, OPTIONS
    import math
    from bukdpxy import sum_last_numerical_value_in_each_row
    from nrmlbukdpxy import sum_last_numerical_value_in_each_row_nrml
    from swchpxy import analyze_stock
    import telegram
    import asyncio
    from selfpxy import get_random_spiritual_message
    from macdpxy import calculate_macd_signal
    macd = calculate_macd_signal("^NSEI")
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
    #SILVER = "\033[97m"
    #UNDERLINE = "\033[4m"
    #RESET = "\033[0m"
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
    from nftpxy import nse_action, nse_power, OPTIONS  
    threshold = 3
###########################################################################################################################################################################################################
    nse_factor = {"Bearish": 0.5, "Bear": 1.0, "Bull": 1.5, "Bullish": 2.0}.get(nse_action, 1.0) 
    options_nse_factor = {"Bearish": 2.0, "Bear": 1.5, "Bull": 0.10, "Bullish": 0.5}.get(nse_action, 1.0)  
    exp_nse_factor = math.exp(options_nse_factor)
    from smapowerpxy import check_smapower_status 
    cepower, pepower = check_smapower_status('^NSEI')
    def assign_otpl(row):
        if 'CE' in row['key']:
            return cepower
        elif 'PE' in row['key']:
            return pepower
        else:
            return None  # Or any default value you prefer
    from smapxy import check_index_status
    SMAfty = check_index_status('^NSEI')
###########################################################################################################################################################################################################
    # Apply the function to create/update the otPL% column
    from depthpxy import calculate_consecutive_candles
    cedepth, pedepth = calculate_consecutive_candles('^NSEI')
    combined_df['otPL%'] = (3 + combined_df.apply(lambda row: pedepth * 0.5 if row['key'].endswith('PE') else cedepth * 0.5  if row['key'].endswith('CE') else None, axis=1))
    combined_df['fPL%'] = combined_df['smb_power'].apply(lambda x: round(np.exp(np.clip(((x + nse_power) / 2), -threshold, threshold)), 2))
    combined_df['tPL%'] = np.round(np.maximum(combined_df['fPL%'], np.maximum(1.4, np.round(np.exp(np.clip(((combined_df['fPL%'] + nse_power) / 2), -threshold, threshold)), 2)) * nse_factor), 2)
    combined_df['tPL%'] = np.where(SMAfty == 'up', np.maximum(1 * combined_df['tPL%'], 1.4), np.where(SMAfty == 'down', np.maximum(combined_df['tPL%'] * 0.5, 1.4), combined_df['tPL%']))
###########################################################################################################################################################################################################
    # Calculate 'Invested' column
    combined_df['Invested'] = (combined_df['qty'] * combined_df['average_price']).round(0).astype(int)
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

###########################################################################################################################################################################################################    
    # Round all numeric columns to 2 decimal places
    numeric_columns = ['fPL%','tPL%','smb_power','oPL%','otPL%','qty', 'average_price', 'Invested','Yvalue', 'ltp','close', 'open', 'high', 'low','value', 'PnL', 'PL%','PL%_H', 'dPnL', 'dPL%']
    combined_df[numeric_columns] = combined_df[numeric_columns].round(2)        # Filter combined_df
    filtered_df = combined_df[((combined_df['product'].isin(['NRML', 'MIS'])) & combined_df['key'].str.startswith('NFO')) | ((combined_df['product'].isin(['CNC', 'MIS'])) & (combined_df['qty'] != 0))]
    # Filter combined_df for rows where 'qty' is greater than 0
    combined_df_positive_qty = combined_df[(combined_df['qty'] > 0) & (combined_df['source'] == 'holdings')]
    # Calculate and print the sum of 'PnL' values and its total 'PL%' for rows where 'qty' is greater than 0
    total_PnL = round(combined_df_positive_qty['PnL'].sum())
    total_PnL_percentage = (total_PnL / combined_df_positive_qty['Invested'].sum()) * 100 if combined_df_positive_qty['Invested'].sum() != 0 else 0   
    # Calculate total_PnL_percentage_options_buy
    stocks_buy_df = combined_df.loc[(combined_df['product'] == "CNC") & (combined_df['qty'] > 0) & (combined_df['source'] == "positions")]
    total_PnL_stocks_buy = round(stocks_buy_df['PnL'].sum()) if not stocks_buy_df.empty else 0    
    options_buy_df = combined_df.loc[(combined_df['product'] == "NRML")]
    total_PnL_options_buy = round(options_buy_df['PnL'].sum()) if not options_buy_df.empty else 0
    total_invested__nrml = options_buy_df['Invested'].sum() if not options_buy_df.empty else 0
    options_percentage_return = round((total_PnL_options_buy / total_invested__nrml) * 100, 0) if total_invested__nrml != 0 else 0
    # Calculate and print the sum of 'dPnL' values and its total 'dPL%' for rows where 'qty' is greater than 0
    #total_dPnL = combined_df_positive_qty['dPnL'].sum()
    total_dPnL = round(combined_df_positive_qty['dPnL'].sum())
    total_dPnL_percentage = (total_dPnL / combined_df_positive_qty['Invested'].sum()) * 100 if combined_df_positive_qty['Invested'].sum() != 0 else 0
    total_dPnL = round(combined_df_positive_qty['dPnL'].sum())

###########################################################################################################################################################################################################    import numpy as np
    
    # Check if the DataFrame is not empty
    import numpy as np
    
    # Check if the DataFrame is not empty
    if not filtered_df.empty:
        # Ensure 'm2m' column is added and replace non-finite values with a default value
        m2m_index = filtered_df.columns.get_loc('m2m')
        filtered_df['m2m'] = filtered_df.iloc[:, m2m_index].replace([np.inf, -np.inf, np.nan], 0).astype(int)
    
        # Filter out rows with NaN values in the 'key' column
        filtered_df = filtered_df.dropna(subset=['key'])
    
        # Group by strike price and sum investments for Put and Call options
        grouped_df = filtered_df.groupby(filtered_df['key'].str.extract(r'(\d+)').squeeze().astype(float).astype('Int64'))
        combined_df = grouped_df.agg({
            'Invested': 'sum',
        }).reset_index()
    
        # Find CE target as same investment as PE for each strike price
        for index, row in combined_df.iterrows():
            strike_price = row['key']
            pe_investment = filtered_df.loc[filtered_df['key'] == f'N{strike_price}PE', 'Invested'].sum()
            ce_investment = filtered_df.loc[filtered_df['key'] == f'N{strike_price}CE', 'Invested'].sum()
            ce_target = pe_investment
            print(f"For CE with strike price {strike_price}, the target investment is: {ce_target}")
    else:
        print(YELLOW + "Filtered DataFrame is empty." + RESET)


    
###########################################################################################################################################################################################################
    import numpy as np
    
    if not combined_df.empty:
        m2m_index = combined_df.columns.get_loc('m2m')
        # Replace non-finite values with a default value (e.g., 0)
        filtered_df['m2m'] = combined_df.iloc[:, m2m_index].replace([np.inf, -np.inf, np.nan], 0)
        # Convert the column to integers
        filtered_df['m2m'] = filtered_df['m2m'].astype(int)
    else:
        print(YELLOW + "Combined DataFrame is empty." + RESET)
    
    # Filter only rows where 'key' starts with 'NFO'
    filtered_df = filtered_df[filtered_df['key'].str.startswith('NFO')]
    
    # After ensuring 'm2m' column is added and rows are filtered, proceed with the rest of the code
    if not filtered_df.empty:
        # Apply transformations
        filtered_df.loc[:, 'option_power'] = filtered_df['smb_power'].apply(lambda smb_power: '⚪' if smb_power > 0.8 else ('🟢' if 0.5 < smb_power <= 0.8 else ('🟠' if 0.3 < smb_power <= 0.5 else ('🔴' if smb_power <= 0.3 else smb_power))))
        filtered_df['key'] = filtered_df['key'].str.replace('NFO:NIFTY', 'N')
    
        # Replace non-finite values in 'PL%' column with 0
        filtered_df['PL%'] = filtered_df['PL%'].fillna(0)
    
        # Convert 'PL%' column to integer
        filtered_df.loc[:, 'PL%'] = filtered_df['PL%'].astype(int)
    
        filtered_df.loc[filtered_df['key'].str.endswith('CE'), 'key'] = filtered_df.loc[filtered_df['key'].str.endswith('CE'), 'key'] + '🟥 '
        filtered_df.loc[filtered_df['key'].str.endswith('PE'), 'key'] = filtered_df.loc[filtered_df['key'].str.endswith('PE'), 'key'] +  '🟩 '
    
        filtered_df = filtered_df.sort_values(by='PL%')
    
        for index, row in filtered_df.iterrows():
            if row['product'] == 'MIS':
                filtered_df.at[index, 'product'] = '⌛'
            elif row['product'] == 'NRML':
                filtered_df.at[index, 'product'] = '⏰'
    
        formatted_lines = filtered_df[['key', 'Invested', 'qty','m2m', 'PnL']].to_string(index=False, header=False).split('\n')
        max_width = 42
        for line in formatted_lines:
            values = line.split()
            pnl_value_str = values[-1]
            try:
                pnl_value = float(pnl_value_str)
            except ValueError:
                pnl_value = None
            if pnl_value is not None:
                if pnl_value > 0:
                    color_code = GREEN
                elif pnl_value < 0:
                    color_code = RED
                elif pnl_value == 0:
                    color_code = YELLOW
                else:
                    color_code = RESET
            else:
                color_code = RESET
            print(color_code + (line[:-3] + line[-3:].rjust(3)).rjust(41) + RESET)
    else:
        print(YELLOW + "..............no options yet in the swing." + RESET)
###########################################################################################################################################################################################################

except Exception as e:
    remove_token(dir_path)
    print(traceback.format_exc())
    logging.error(f"{str(e)} in the main loop")
