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
from cmbddfpxy import process_data
combined_df = process_data()
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
def stocks_sell_order_place(index, row):
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
                price=round_to_paise(row['ltp'], -0.2)
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
                        columns_to_drop = ['fPL%','tPL%','oPL%','smb_power', 'oPL%', 'pstp', '_pstp', 'qty', 'close', 'open', 'high', 'low', 'dPL%', 'pxy','yxp']
                        # Dropping specified columns from the row
                        for column in columns_to_drop:
                            if column in row:
                                del row[column]
                        message_text = f"{str(row):>10} \nhttps://www.tradingview.com/chart/?symbol={key}\nBooked profit until now: {result}"
                        # Define the bot token and your Telegram username or ID
                        bot_token = '6867988078:AAGNBJqs4Rf8MR4xPGoL1-PqDOYouPan7b0'  # Replace with your actual bot token
                        user_usernames = ('-4136531362')  # Replace with your Telegram username or ID
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
def stocks_avg_order_place(index, row):
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
            qty = 1 if row['ltp'] > 1000 else 1000 // row['ltp']
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
                    bot_token = '6924826872:AAHTiMaXmjyYbGsCFhdZlRRXkyfZTpsKPug'  # Replace with your actual bot token
                    user_id = '-4135910842'  # Replace with your Telegram user ID
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
    file_path = 'filePnL.csv'
    result = sum_last_numerical_value_in_each_row(file_path)  
    file_path_nrml = "filePnL_nrml.csv"
    result_nrml = sum_last_numerical_value_in_each_row_nrml(file_path_nrml)

###########################################################################################################################################################################################################
    try:
        response = broker.kite.margins()
        available_cash = response["equity"]["available"]["live_balance"]
    except Exception as e:
        print(f"An error occurred: {e}")
        available_cash = 0
###########################################################################################################################################################################################################
    epsilon = 1e-10
    combined_df[['smb_power']] = combined_df.apply(
        lambda row: pd.Series({'smb_power': round(abs(row['ltp'] - (row['low'] - 0.01)) / (abs(row['high'] + 0.01) - abs(row['low'] - 0.01) + epsilon) if (abs(row['high'] + 0.01) - abs(row['low'] - 0.01) + epsilon != 0) and (row['ltp'] - (row['low'] - 0.01) != 0) else 0.5, 2)}), 
        axis=1
    )
    from nftpxy import nse_action, nse_power, OPTIONS  
    threshold = 3
###########################################################################################################################################################################################################
    from smapxy import check_index_status
    SMAfty = check_index_status('^NSEI')
###########################################################################################################################################################################################################
    combined_df['fPL%'] = combined_df['smb_power'].apply(lambda x: round(np.exp(np.clip(((x + nse_power) / 2), -threshold, threshold)), 2))
    combined_df['tPL%'] = np.round(np.maximum(combined_df['fPL%'], np.maximum(1.4, np.round(np.exp(np.clip(((combined_df['fPL%'] + nse_power) / 2), -threshold, threshold)), 2)) * 1), 2)
    combined_df['tPL%'] = np.where(SMAfty == 'up', np.maximum(1 * combined_df['tPL%'], 1.4), np.where(SMAfty == 'down', np.maximum(combined_df['tPL%'] * 0.5, 1.4), combined_df['tPL%']))
###########################################################################################################################################################################################################
    import pandas as pd
    import numpy as np
    
    if not combined_df.empty:
        if 'm2m' in combined_df.columns:
            m2m_index = combined_df.columns.get_loc('m2m')
            if not combined_df['m2m'].isnull().all():
                combined_df['m2m'] = combined_df.iloc[:, m2m_index].replace([np.inf, -np.inf, np.nan], 0)
                combined_df['m2m'] = combined_df['m2m'].astype(int)
            else:
                m2m_index = 0  # Set m2m_index to 0 if all values in 'm2m' column are empty
        else:
            #print("Warning: 'm2m' column not found.")
            # If 'm2m' column doesn't exist, you can add it with default values or handle it accordingly
            combined_df['m2m'] = 0  # For example, you can add 'm2m' column with default value 0
        
        m2m_filtered_df = combined_df[(combined_df['source'] == 'positions') & (combined_df['qty'] > 0)]
        
        # Check if 'm2m' column exists in m2m_filtered_df before accessing it
        if 'm2m' in m2m_filtered_df.columns:
            total_postions_m2m = m2m_filtered_df['m2m'].sum()
        else:
            #print("Warning: 'm2m' column not found in filtered DataFrame.")
            total_postions_m2m = 0  # or any other appropriate value
   
    else:
        total_postions_m2m = 0
        #print("Combined DataFrame is empty.")

###########################################################################################################################################################################################################    
    # Round all numeric columns to 2 decimal places
    numeric_columns = ['fPL%','tPL%','smb_power','oPL%','qty', 'average_price', 'Invested','Yvalue', 'ltp','close', 'open', 'high', 'low','value', 'PnL', 'PL%', 'dPnL', 'dPL%']
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
###########################################################################################################################################################################################################

    import pandas as pd
    from tabulate import tabulate
    # Define the file path for the CSV file
    lstchk_file = "fileHPdf.csv"
    # Dump the DataFrame to the CSV file, overwriting any existing file
    combined_df.to_csv(lstchk_file, index=False)
    #print(f"DataFrame has been saved to {lstchk_file}")
    # Create a copy of 'filtered_df' and select specific columns
    pxy_df = filtered_df.copy()[['fPL%','tPL%','smb_power','oPL%','Invested','source','product', 'qty','average_price', 'close', 'ltp', 'open', 'high','low','key','dPL%','PnL', 'PL%']]
    pxy_df['avg'] =filtered_df['average_price']
    # Create a copy for just printing 'filtered_df' and select specific columns
    EXE_df = pxy_df[['tPL%','fPL%','smb_power','oPL%','Invested','qty', 'avg', 'close', 'ltp', 'open', 'high', 'low',  'dPL%','product', 'source', 'key', 'PL%', 'PnL']]    
    PRINT_df = pxy_df[(pxy_df['qty'] > 0) & (~pxy_df['key'].str.contains('NFO'))][['source', 'key', 'dPL%', 'oPL%', 'tPL%', 'smb_power', 'PL%', 'PnL']]
    # Rename columns for display
    PRINT_df = PRINT_df.rename(columns={'source': 'HP', 'smb_power': 'TR','key': 'key','dPL%': 'dPL%'})
    # Conditionally replace values in the 'HP' column
    PRINT_df['HP'] = PRINT_df['HP'].replace({'holdings': '📌', 'positions': '🎯'})
    # Conditionally replace values in the '_CM' column
    #PRINT_df['_CM'] = PRINT_df['_CM'].replace({'CNC': '🧰', 'MIS': '⌛','NRML': '💸'}) 
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
    PRINT_df_sorted['key'] = PRINT_df_sorted['key'].str.replace(r'(BSE:|NSE:|NFO:)', '', regex=True).str[:8].str.ljust(8, ' ')
    # Sort the DataFrame by 'PL%' in ascending order
    PRINT_df_sorted = PRINT_df_sorted.sort_values(by='PL%', ascending=True)
    # Convert the 'PL%' column to integers
    #PRINT_df_sorted.loc[:, 'PL%'] = PRINT_df_sorted['PL%'].astype(int)
    # ANSI escape codes for text coloring
    #RESET = "\033[0m"
    #BRIGHT_YELLOW = "\033[93m"
    # Set the maximum width for all columns
    pd.set_option('display.max_colwidth', 1)  # Adjust the value for your desired width
    # Apply truncation to each cell in the DataFrame
    PRINT_df_sorted_display = PRINT_df_sorted.copy()
    #print("━" * 42)
    # Always print "Table" in bright yellow
    # Print the truncated DataFrame without color
    # Assuming PRINT_df_sorted_display is your DataFrame
    stocks_filtered_df = PRINT_df_sorted_display[PRINT_df_sorted_display['PL%'] > 1.4].sort_values(by='PL%')
###########################################################################################################################################################################################################   
    from mktrndpxy import get_market_status_for_symbol
    importlib.reload(sys.modules['mktrndpxy'])
    nmktpxy = get_market_status_for_symbol('^NSEI')
    from mktpxy import get_market_check
    importlib.reload(sys.modules['mktpxy'])  # Correct the usage
    onemincandlesequance, mktpxy = get_market_check('^NSEI')
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
                         row['PL%'] > 1.4 ) and
                        (
                            (row['PL%'] > row['tPL%']) or ((row['PL%'] > 0) and (total_dPnL < 0))
                        )
                    ):
                        try:
                            is_placed = stocks_sell_order_place(key, row) if get_open_order_status(symbol_in_order) == "NO" else False
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
                         available_cash > 10000 and
                         nse_power < 0.1 and
                         mktpxy in ['Buy', 'Bull'] and
                         row['PL%'] < -20)
                    ):
                        try:                            
                            is_placed = stocks_avg_order_place(key, row) if get_open_order_status(symbol_in_order) == "NO" else False
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
    from smapxy import check_index_status
    nsma = check_index_status("^NSEI")
    from dshpxy import get_holdingsinfo
    total_nrml_m2m, total_cnc_m2m, all_Stocks_count, red_Stocks_count, green_Stocks_count, all_Stocks_capital_lacks, all_Stocks_worth_lacks, zero_qty_count, green_Stocks_profit_loss, green_Stocks_capital_rercentage,nrmlall_Stocks_count ,nrmlall_Stocks_capital ,nrmlall_Stocks_worth ,nrmlall_Stocks_profit_loss = get_holdingsinfo(combined_df)    
    from bordpxy import printbord
    printbord(total_nrml_m2m, total_cnc_m2m, optpxy, Day_Change, result, total_PnL_percentage, total_dPnL, total_PnL, total_dPnL_percentage,
             result_nrml, total_PnL_stocks_buy, total_PnL_options_buy, available_cash,
             nse_power,all_Stocks_count, red_Stocks_count,green_Stocks_count,all_Stocks_capital_lacks,all_Stocks_worth_lacks, zero_qty_count, green_Stocks_profit_loss, green_Stocks_capital_rercentage, mktpxy,nrmlall_Stocks_count ,nrmlall_Stocks_capital ,nrmlall_Stocks_worth ,nrmlall_Stocks_profit_loss, nsma)
###########################################################################################################################################################################################################
    if not stocks_filtered_df.empty:
        print('\n'.join([line.rjust(40) for line in stocks_filtered_df.to_string(index=False, header=False).split('\n')]))
        print((GREEN if nsma == "up" else RED if nsma == "down" else YELLOW) + "ﮩ٨ﮩ٨ـﮩ٨ﮩ٨ـﮩ٨ـﮩﮩ٨ﮩ٨ـﮩ٨ﮩ٨ـﮩ٨ـﮩﮩ٨ﮩ٨ـﮩ٨ﮩ٨ـﮩ٨ـﮩ" + RESET)
###########################################################################################################################################################################################################
except Exception as e:
    remove_token(dir_path)
    print(traceback.format_exc())
    logging.error(f"{str(e)} in the main loop")
