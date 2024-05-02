###################################################################################"PXY® PreciseXceleratedYield Pvt Ltd™########################################################################################################################
import pandas as pd
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
from cmbddfpxy import process_data
combined_df = process_data()
from clorpxy import SILVER, UNDERLINE, RED, GREEN, YELLOW, RESET, BRIGHT_YELLOW, BRIGHT_RED, BRIGHT_GREEN, BOLD, GREY
###################################################################################"PXY® PreciseXceleratedYield Pvt Ltd™########################################################################################################################
file_path = 'filePnL.csv'
booked = sum_last_numerical_value_in_each_row(file_path)  
###################################################################################"PXY® PreciseXceleratedYield Pvt Ltd™########################################################################################################################
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
####################################################################################"PXY® PreciseXceleratedYield Pvt Ltd™#######################################################################################################################
def get_any_order_status(symbol):
    try:
        orders = broker.kite.orders()
        for order in orders:
            if order['tradingsymbol'] == symbol:
                return "YES"  # There is at least one order for the symbol
    except Exception as e:
        logging.error(f"Error fetching orders: {str(e)}")
        return "ERROR"  # Unable to fetch orders due to error
    return "NO"  # No orders found for the symbol
####################################################################################"PXY® PreciseXceleratedYield Pvt Ltd™#######################################################################################################################
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
#####################################################################################"PXY® PreciseXceleratedYield Pvt Ltd™######################################################################################################################
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
######################################################################################"PXY® PreciseXceleratedYield Pvt Ltd™#####################################################################################################################            
            if order_id:
                logging.info(f"Order {order_id} placed for {exchsym[1]} successfully")                                
                with open(csv_file_path, 'a', newline='') as csvfile:
                    csvwriter = csv.writer(csvfile)
                    csvwriter.writerow(row.tolist())  # Write the selected row to the CSV file
                    try:
                        import telegram
                        import asyncio
                        columns_to_drop = ['fPL%','smb_power','oPL%', 'qty', 'close',  'open', 'high', 'low', 'dPL%','product']
                        for column in columns_to_drop:
                            if column in row:
                                del row[column]
                        message_text = f"📊 Let's Book {exchsym[1]}!\n💰 Profit: {row['PnL']}\n💹 Profit %: {row['PL%']}\n🔢 H/P: {row['source']}\n📈 LTP: {row['ltp']}\n📉 Avg: {row['avg']}\n🔍 Check it out on TradingView: https://www.tradingview.com/chart/?symbol={exchsym[1]}\nBooked profit until now: {booked}"
                        bot_token = '6867988078:AAGNBJqs4Rf8MR4xPGoL1-PqDOYouPan7b0'  # Replace with your actual bot token
                        user_usernames = ('-4136531362')  # Replace with your Telegram username or ID
                        # Function to send a message to Telegram
                        async def send_telegram_message(message_text):
                            bot = telegram.Bot(token=bot_token)
                            await bot.send_message(chat_id=user_usernames, text=message_text)
                    except Exception as e:
                        print(f"Error sending message to Telegram: {e}")
                    loop = asyncio.get_event_loop()
                    loop.run_until_complete(send_telegram_message(message_text))
                return True                
            else:
                logging.error("Order placement failed")       
        else:
            logging.error("Invalid format for 'index'")    
    except Exception as e:
        logging.error(f"{str(e)} while placing order")
    return False
############################################################################################"PXY® PreciseXceleratedYield Pvt Ltd™###############################################################################################################
def stocks_avg_order_place(index, row):
    try:
        exchsym = str(index).split(":")
        positions_response = broker.kite.positions()
        open_positions = positions_response.get('net', [])
        existing_position = next((position for position in open_positions if position['tradingsymbol'] == exchsym[1]), None)
        if existing_position:
            logging.info(f"Position already exists for {exchsym[1]}. Skipping order placement.")
            return True
        if len(exchsym) >= 2 :
            logging.info(f"Placing order for {exchsym[1]}, {str(row)}")
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
                try:
                    message_text = f"📊 Let's Average {exchsym[1]}!\n📈 Current Price (LTP): {row['ltp']}\n💰 Investment: {row['Invested']}\n📉 Avg: {row['avg']}\n🔍 Check it out on TradingView: https://www.tradingview.com/chart/?symbol={exchsym[1]}"
                    bot_token = '6924826872:AAHTiMaXmjyYbGsCFhdZlRRXkyfZTpsKPug'  # Replace with your actual bot token
                    user_id = '-4135910842'  # Replace with your Telegram user ID
                    async def send_telegram_message(message_text):
                        bot = telegram.Bot(token=bot_token)
                        await bot.send_message(chat_id=user_id, text=message_text)
                    asyncio.run(send_telegram_message(message_text))
                except Exception as e:
                    print(f"Error sending message to Telegram: {e}")
                return exchsym[1], remaining_cash  # Define remaining_cash appropriately
            return True
        else:
            logging.error("Order placement failed")
    except Exception as e:
        logging.error(f"{str(e)} while placing order")
    return False
###################################################################################"PXY® PreciseXceleratedYield Pvt Ltd™########################################################################################################################
try:
    import sys
    import traceback
    import pandas as pd
    import datetime
    import time
    from login_get_kite import get_kite, remove_token
    from cnstpxy import dir_path, sellbuff, secs, perc_col_name
    from toolkit.logger import Logger
    from toolkit.currency import round_to_paise
    import csv
    from time import sleep
    import subprocess
    import random
    import os
    import numpy as np
    from mktpxy import get_market_check
    import importlib
    from nftpxy import ha_nse_action, nse_power, Day_Change, Open_Change  
    import math
    from bukdpxy import sum_last_numerical_value_in_each_row
    from swchpxy import analyze_stock
    import telegram
    import asyncio
    from selfpxy import get_random_spiritual_message
    from macdpxy import calculate_macd_signal
    from smapxy import check_index_status
    from tabulate import tabulate
    from dshpxy import get_holdingsinfo
    from bordpxy import printbord
    from utcpxy import peak_time
###################################################################################"PXY® PreciseXceleratedYield Pvt Ltd™########################################################################################################################
    onemincandlesequance, mktpxy = get_market_check('^NSEI')
    macd = calculate_macd_signal("^NSEI")
    random_message = get_random_spiritual_message()
    switch = analyze_stock()
    file_path = 'filePnL.csv'
    booked = sum_last_numerical_value_in_each_row(file_path)  
    nsma = check_index_status('^NSEI')
    peak = peak_time()
####################################################################################"PXY® PreciseXceleratedYield Pvt Ltd™#####################################################################################################################
    try:
        response = broker.kite.margins()
        available_cash = response["equity"]["available"]["live_balance"]
    except Exception as e:
        print(f"An error occurred: {e}")
        available_cash = 0
###################################################################################"PXY® PreciseXceleratedYield Pvt Ltd™########################################################################################################################
    epsilon = 1e-10
    def calculate_smb_power(row):
        start = row['low'] if row['source'] == 'holdings' else (row['avg'] if row['source'] == 'positions' else ValueError("Invalid value in 'source' column"))
        smb_power = round(abs(row['ltp'] - (start - 0.01)) / (abs(row['high'] + 0.01) - abs(start - 0.01) + epsilon), 2)
        if abs(row['high'] + 0.01) - abs(start - 0.01) + epsilon != 0 and row['ltp'] - (start - 0.01) != 0:
            return smb_power
        else:
            return 0.5
    combined_df['smb_power'] = combined_df.apply(calculate_smb_power, axis=1)
    threshold = 3
###################################################################################"PXY® PreciseXceleratedYield Pvt Ltd™########################################################################################################################
    combined_df['fPL%'] = combined_df['smb_power'].apply(lambda x: round(np.exp(np.clip(((x + x) / 2), -threshold, threshold)), 2))
    combined_df['tPL%'] = np.maximum(combined_df['fPL%'], np.maximum(1.4, np.round(np.exp(np.clip(((combined_df['fPL%'] + combined_df['fPL%']) / 2), -threshold, threshold)), 2)) * 1)
    combined_df['tPL%'] = np.where(nsma == 'up', np.maximum(1 * (combined_df['tPL%'] * nse_power), 1.4), np.where(nsma == 'down', np.maximum((combined_df['tPL%'] * nse_power) * 0.5, 1.4), 1.4)) + 1.4
###################################################################################"PXY® PreciseXceleratedYield Pvt Ltd™########################################################################################################################
    numeric_columns = ['fPL%','tPL%','smb_power','oPL%','qty', 'average_price', 'Invested','Yvalue', 'ltp','close', 'open', 'high', 'low','value', 'PnL', 'PL%', 'dPnL', 'dPL%']
    combined_df[numeric_columns] = combined_df[numeric_columns].round(2)
    total_opt_real = combined_df[(combined_df['qty'] == 0) & (combined_df['key'].str.contains('NFO:'))]['pnl'].sum()
    filtered_df = combined_df[(combined_df['product'] == 'CNC') & (combined_df['qty'] != 0)]
####################################################################################"PXY® PreciseXceleratedYield Pvt Ltd™#######################################################################################################################
    result = get_holdingsinfo(combined_df)
    if result is not None:
        extras, optworth, all_Stocks_worth_dpnl, all_Stocks_yworth_lacks, total_cnc_m2m, all_Stocks_count, red_Stocks_count, green_Stocks_count, all_Stocks_capital_lacks, all_Stocks_worth_lacks, zero_qty_count, green_Stocks_profit_loss, green_Stocks_capital_percentage = result
    else:
        # Handle the case where get_holdingsinfo returns None
        print("Error: Unable to retrieve holdings information.")
    extras, optworth, all_Stocks_worth_dpnl, all_Stocks_yworth_lacks, total_cnc_m2m, all_Stocks_count, red_Stocks_count, green_Stocks_count, all_Stocks_capital_lacks, all_Stocks_worth_lacks, zero_qty_count, green_Stocks_profit_loss, green_Stocks_capital_percentage = get_holdingsinfo(combined_df)    
####################################################################################"PXY® PreciseXceleratedYield Pvt Ltd™#######################################################################################################################
    lstchk_file = "fileHPdf.csv"
    combined_df.to_csv(lstchk_file, index=False)
    pxy_df = filtered_df.copy()[['tPL%','fPL%','oPL%','dPL%','PnL', 'PL%','smb_power','Invested','source','product', 'qty','avg','ltp', 'open', 'high', 'close', 'low','key']]
    pxy_df['avg'] =filtered_df['average_price']
    EXE_df = pxy_df[['tPL%','fPL%','smb_power','smb_power','smb_power','oPL%','Invested','qty', 'avg', 'close', 'ltp', 'open', 'high', 'low', 'dPL%','product', 'source', 'key', 'PL%', 'PnL']]    
    PRINT_df = pxy_df[(pxy_df['qty'] > 0) & (~pxy_df['key'].str.contains('NFO'))][['source', 'key', 'dPL%', 'oPL%', 'tPL%', 'smb_power', 'PL%', 'PnL']]
    PRINT_df = PRINT_df.rename(columns={'source': 'HP', 'smb_power': 'TR','key': 'key','dPL%': 'dPL%'})
    PRINT_df['HP'] = PRINT_df['HP'].replace({'holdings': '📌', 'positions': '🎯'})
    PRINT_df['TR'] = PRINT_df['TR'].apply(lambda TR: '⚪' if TR > 0.8 else ('🟢' if 0.5 < TR <= 0.8 else ('🟠' if 0.3 < TR <= 0.5 else ('🔴' if TR <= 0.3 else TR))))
    PRINT_df['key'] = PRINT_df['key'].str.replace(r'BSE:|NSE:', '', regex=True)
########################################################################################"PXY® PreciseXceleratedYield Pvt Ltd™###################################################################################################################    
    PRINT_df_sorted = PRINT_df.copy()
    PRINT_df_sorted['TR'] = PRINT_df_sorted['TR'].apply(lambda TR: TR[:2] if isinstance(TR, str) else TR)
    PRINT_df_sorted['key'] = PRINT_df_sorted['key'].str.replace(r'(BSE:|NSE:|NFO:)', '', regex=True).str[:7].str.ljust(7, ' ')
    PRINT_df_sorted = PRINT_df_sorted.sort_values(by='PL%', ascending=True)
    pd.set_option('display.max_colwidth', 1)
    PRINT_df_sorted_display = PRINT_df_sorted.copy()
    stocks_filtered_df = PRINT_df_sorted_display[PRINT_df_sorted_display['PL%'] > (PRINT_df_sorted_display['tPL%'] * 0.50)].sort_values(by='PL%')
########################################################################################"PXY® PreciseXceleratedYield Pvt Ltd™###################################################################################################################   
    csv_file_path = "filePnL.csv"
    total_dPnL = ((all_Stocks_worth_lacks - all_Stocks_yworth_lacks)*100000)
    selected_rows = []
    if mktpxy == "Sell" or mktpxy == "Bear":
        try:
            for index, row in EXE_df.iterrows():
                excluded_keys = set(pd.read_csv("filePnL.csv", header=None).iloc[:, -3])
                key = row['key']  # Get the 'key' value
                symbol_in_order = row['key'].split(":")[1]
                if (
                    row['key'] not in excluded_keys and
                    row['open'] > 0 and
                    row['high'] > 0 and
                    row['low'] > 0 and
                    row['close'] > 0 and
                    nse_power != 0.50 and
                    row['ltp'] != 0 
                ):                            
############################################################################################"PXY® PreciseXceleratedYield Pvt Ltd™###############################################################################################################                    
                    if (
                        (row['qty'] > 0 and
                         row['avg'] != 0 and
                         row['product'] == 'CNC' and
                         row['PL%'] > 1.4) and
                        (
                            (((row['PL%'] > row['tPL%']) and (row['PnL'] > 200 )) or (total_dPnL < 0 and (row['oPL%'] < 0 ) and row['source'] == 'holdings'))
                        )
                    ):
                        try:
                            is_placed = stocks_sell_order_place(key, row) if get_open_order_status(symbol_in_order) == "NO" else False
                            if is_placed:
                                print(row)  # Optionally print the row after placing the order
                        except Exception as e:
                            # Handle any other exceptions that may occur during order placement
                            print(f"An unexpected error occurred while placing an order for key {key}: {e}")
##############################################################################################"PXY® PreciseXceleratedYield Pvt Ltd™#############################################################################################################     
                    elif (
                        (row['qty'] > 0 and
                         row['avg'] != 0 and
                         row['Invested'] < 20000 and
                         available_cash > 1000 and
                         peak == 'PEAKEND' and
                         row['PL%'] < -20)
                    ):
                        try:                            
                            is_placed = stocks_avg_order_place(key, row) if get_any_order_status(symbol_in_order) == "NO" else False
                            if is_placed:
                                print(row['key'])                                
                        except Exception as e:
                            # Handle any other exceptions that may occur during order placement
                            print(f"An unexpected error occurred while placing an order for key {key}: {e}")
        except Exception as e:
            # Handle any other exceptions that may occur during the loop
            print(f"An unexpected error occurred: {e}")   
###########################################################################################################################################################################################################  
    if not stocks_filtered_df.empty:
        print('\n'.join([line.rjust(40) for line in stocks_filtered_df.to_string(index=False, header=False).split('\n')]))    
    print("━" * 42)
############################################################################################"PXY® PreciseXceleratedYield Pvt Ltd™###############################################################################################################
    printbord(extras, optworth, all_Stocks_worth_dpnl, nsma, all_Stocks_yworth_lacks, total_cnc_m2m, mktpxy, available_cash, ha_nse_action, nse_power, Day_Change, Open_Change, all_Stocks_count, red_Stocks_count, green_Stocks_count, all_Stocks_capital_lacks, all_Stocks_worth_lacks, zero_qty_count, green_Stocks_profit_loss, green_Stocks_capital_percentage)
#############################################################################################"PXY® PreciseXceleratedYield Pvt Ltd™##############################################################################################################
except Exception as e:
    remove_token(dir_path)
    print(traceback.format_exc())
    logging.error(f"{str(e)} in the main loop")
#############################################################################################"PXY® PreciseXceleratedYield Pvt Ltd™##############################################################################################################
