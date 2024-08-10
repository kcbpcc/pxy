###################################################################################"PXY® PreciseXceleratedYield Pvt Ltd™########################################################################################################################
#print("━" * 42)
import argparse
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
from cmbddfpxy import process_data
combined_df = process_data()
from prftpxy import process_data_total_profit
booked = process_data_total_profit()
from clorpxy import SILVER, UNDERLINE, RED, GREEN, YELLOW, RESET, BRIGHT_YELLOW, BRIGHT_RED, BRIGHT_GREEN, BOLD, GREY
###################################################################################"PXY® PreciseXceleratedYield Pvt Ltd™########################################################################################################################
# Parse command-line arguments
parser = argparse.ArgumentParser(description="Process some commands.")
parser.add_argument('-flash', action='store_true', help="Enable flash mode")
parser.add_argument('-flashFLASH', action='store_true', help="Enable flash mode")
parser.add_argument('-short', action='store_true', help="Enable option S")
args = parser.parse_args()

flash = 'yes' if args.flash else 'no'
runshort = 'yes' if args.short else 'no'
flashFLASH = 'yes' if args.flashFLASH else 'no'
###################################################################################"PXY® PreciseXceleratedYield Pvt Ltd™########################################################################################################################
logging = Logger(30, dir_path + "main.log")
try:
    original_stdout = sys.stdout
    sys.stdout = open('output.txt', 'w')
    broker = get_kite()
except Exception as e:
    sys.stdout = original_stdout
    remove_token(dir_path)
    print(traceback.format_exc())
    logging.error(f"{str(e)} unable to get holdings")
    sys.exit(1)
finally:
    sys.stdout = original_stdout
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
            
            # Assuming broker and round_to_paise are defined elsewhere
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
                
                # Prepare and send Telegram message
                columns_to_drop = ['fPL%', 'smb_power', 'oPL%', 'qty', 'close', 'open', 'high', 'low', 'dPL%', 'product']
                for column in columns_to_drop:
                    if column in row:
                        del row[column]
                
                message_text = (
                    f"📊 Let's Book {exchsym[1]}!\n"
                    f"💰 Profit: {row['PnL']}\n"
                    f"💹 Profit %: {row['PL%']}\n"
                    f"🔢 H/P: {row['source']}\n"
                    f"📉 Sell Price: {row['ltp']}\n"
                    f"📈 Buy Price: {row['avg']}\n"
                    f"🔍 Check it out on TradingView: https://www.tradingview.com/chart/?symbol={exchsym[1]}\n"
                    f"Profits until:{booked} 📣"
                )
                
                bot_token = '6867988078:AAGNBJqs4Rf8MR4xPGoL1-PqDOYouPan7b0'  # Replace with your actual bot token
                user_usernames = ('-4136531362')  # Replace with your Telegram username or ID
                
                async def send_telegram_message(message_text):
                    bot = telegram.Bot(token=bot_token)
                    await bot.send_message(chat_id=user_usernames, text=message_text)
                
                loop = asyncio.get_event_loop()
                loop.run_until_complete(send_telegram_message(message_text))
                
                return True
            else:
                logging.error("Order placement failed")
        else:
            logging.error("Invalid format for 'index'")
    except Exception as e:
        logging.error(f"Error: {str(e)} while placing order")
    
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
            qty = 1 if row['ltp'] > 1000 else (1000 // row['ltp']) * abs(row['dPL%'])
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
                return exchsym[1]
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
    from cnstpxy import dir_path, secs, perc_col_name
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
    import telegram
    import asyncio
    from macdpxy import calculate_macd_signal
    from smapxy import check_index_status
    from tabulate import tabulate
    from utcpxy import peak_time
###################################################################################"PXY® PreciseXceleratedYield Pvt Ltd™########################################################################################################################
    onemincandlesequance, mktpxy = get_market_check('^NSEI')
    macd = calculate_macd_signal("^NSEI")
    nsma = check_index_status('^NSEI')
    peak = peak_time()
####################################################################################"PXY® PreciseXceleratedYield Pvt Ltd™#####################################################################################################################
    from fundpxy import calculate_decision
    try:
        decision, optdecision, available_cash,live_balance, limit = calculate_decision()
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
    from predictpxy import predict_market_sentiment
    mktpredict = predict_market_sentiment()
    if mktpredict == "RISE":
        nsefactor = 10
    elif mktpredict == "FALL":
        nsefactor = 0
    elif mktpredict == "SIDE":
        nsefactor = 6
    else:
        nsefactor = 5
###################################################################################"PXY® PreciseXceleratedYield Pvt Ltd™########################################################################################################################
    combined_df['fPL%'] = combined_df['smb_power'].apply(lambda x: round(np.exp(np.clip(((x + x) / 2), -threshold, threshold)), 2))
    combined_df['tPL%'] = np.maximum(combined_df['fPL%'], np.maximum(1.4, np.round(np.exp(np.clip(((combined_df['fPL%'] + combined_df['fPL%']) / 2), -threshold, threshold)), 2)) * 1)
    combined_df['tPL%'] = np.where(nsma == 'up', np.maximum(1 * (combined_df['tPL%'] * nse_power), 1.4), np.where(nsma == 'down', np.maximum((combined_df['tPL%'] * nse_power) * 0.5, 1.4), 1.4)) + 1.4 + nsefactor
###################################################################################"PXY® PreciseXceleratedYield Pvt Ltd™########################################################################################################################
    numeric_columns = ['fPL%','tPL%','smb_power','oPL%','qty', 'average_price', 'Invested','Yvalue', 'ltp','close', 'open', 'high', 'low','value', 'PnL', 'PL%', 'dPnL', 'dPL%']
    combined_df[numeric_columns] = combined_df[numeric_columns].round(2)
    total_opt_real = combined_df[(combined_df['qty'] == 0) & (combined_df['key'].str.contains('NFO:'))]['pnl'].sum()
    filtered_df = combined_df[(combined_df['product'] == 'CNC') & (combined_df['qty'] != 0)]
####################################################################################"PXY® PreciseXceleratedYield Pvt Ltd™#######################################################################################################################
    pxy_df = filtered_df.copy()[['tPL%','fPL%','oPL%','dPL%','PnL', 'PL%','smb_power','Invested','source','product', 'qty','avg','ltp', 'open', 'high', 'close', 'low','key']]
    pxy_df['avg'] =filtered_df['average_price']
    EXE_df = pxy_df[['tPL%','fPL%','smb_power','oPL%','Invested','qty', 'avg', 'close', 'ltp', 'open', 'high', 'low', 'dPL%','product', 'source', 'key', 'PL%', 'PnL']]    
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
    stocks_filtered_df = PRINT_df_sorted_display[PRINT_df_sorted_display['PL%'] > 1.4].sort_values(by='PL%')
########################################################################################"PXY® PreciseXceleratedYield Pvt Ltd™###################################################################################################################   
    if not os.path.exists("pxyexclude.csv"):
        df = pd.DataFrame(columns=["STOCK"])
        df.to_csv("pxyexclude.csv", index=False)
    else:
        df = pd.read_csv("pxyexclude.csv")
###################################################################################"PXY® PreciseXceleratedYield Pvt Ltd™########################################################################################################################
    selected_rows = []
    if True:
        try:
            for index, row in EXE_df.iterrows():
                excluded_keys = set(df['STOCK'])
                key = row['key']
                symbol_in_order = key.split(":")[1]
    
                if (
                    symbol_in_order not in excluded_keys and
                    row['open'] > 0 and
                    row['high'] > 0 and
                    row['low'] > 0 and
                    row['close'] > 0 and
                    nse_power != 0.50 and
                    row['ltp'] != 0
                ):
###################################################################################"PXY® PreciseXceleratedYield Pvt Ltd™########################################################################################################################
                    if (
                        row['qty'] > 0 and
                        row['avg'] != 0 and
                        row['product'] == 'CNC' and
                        mktpredict == "FALL" and
                        row['PL%'] > 1.4 and 
                        row['PnL'] > 140 and
                        (mktpxy == "Sell" or mktpxy == "Bear") and
                        (
                            (row['PL%'] > row['tPL%'] and row['PnL'] > 140 and row['PL%'] > 1.4 ) 
                        )
                    ):
                  
                        try:
                            print(f"Trying to close: {row['key']}")
                            is_placed = stocks_sell_order_place(key, row) if get_open_order_status(symbol_in_order) == "NO" else False
                            if is_placed:
                                print(row)  # Optionally print the row after placing the order
                        except Exception as e:
                            # Handle any other exceptions that may occur during order placement
                            print(f"An unexpected error occurred while placing an order for key {key}: {e}")
    ############################################################################################      ############################################################################################    
                    elif (
                        row['qty'] > 0 and
                        row['avg'] != 0 and
                        row['product'] == 'CNC' and
                        (
                            (flash == 'yes' and row['PL%'] > 0 and row['PnL'] > 0) or  # exit only positive 
                            (flashFLASH == 'yes')  # exit everything
                        )
                    ):
                        try:
                            print(f"Trying to close: {row['key']}")
                            is_placed = stocks_sell_order_place(key, row) if get_open_order_status(symbol_in_order) == "NO" else False
                            if is_placed:
                                print(row)  # Optionally print the row after placing the order
                        except Exception as e:
                            print(f"An unexpected error occurred while placing an order for key {key}: {e}")
    ############################################################################################      ############################################################################################    
                    elif (
                        row['qty'] > 0 and
                        row['avg'] != 0 and
                        row['Invested'] < 50000 and
                        available_cash > 1000 and
                        peak == 'PEAKEND' and
                        row['dPL%'] < -1
                    ):
                        try:
                            # Read the stock symbols from stocks.csv
                            stocks_df = pd.read_csv('avgstocks')
                            stock_symbols = stocks_df['Symbol'].tolist()  # Assuming 'Symbol' is the column name in stocks.csv
                    
                            # Define a function to strip the prefix (NSE: or BSE:) from the symbol
                            def strip_prefix(symbol):
                                if ':' in symbol:
                                    return symbol.split(':')[1]
                                return symbol
                    
                            # Extract symbol part after ':' if any
                            symbol_in_order = row['key'].split(":")[1]
                    
                            # Apply the function to strip the prefix from 'key' and check if it is in stock_symbols
                            stripped_symbol = strip_prefix(row['key'])
                            if stripped_symbol in stock_symbols:
                                #print(f"Trying to average: {row['key']}")
                                is_placed = stocks_avg_order_place(key, row) if get_any_order_status(symbol_in_order) == "NO" else False
                                if is_placed:
                                    print(f"Averaged {row['key']}")
                        except Exception as e:
                            # Handle any other exceptions that may occur during order placement
                            print(f"An unexpected error occurred while placing an order for key {key}: {e}")
    
        except Exception as e:
            # Handle any other exceptions that may occur during the loop
            print(f"An unexpected error occurred: {e}")
#############################################################################################"PXY® PreciseXceleratedYield Pvt Ltd™##############################################################################################################
    if not stocks_filtered_df.empty and runshort != 'yes':
        print('\n'.join([line.rjust(40) for line in stocks_filtered_df.to_string(index=False, header=False).split('\n')]))
        #print("━" * 42)
############################################################################################"PXY® PreciseXceleratedYield Pvt Ltd™###############################################################################################################
except Exception as e:
    remove_token(dir_path)
    print(traceback.format_exc())
    logging.error(f"{str(e)} in the main loop")
#############################################################################################"PXY® PreciseXceleratedYield Pvt Ltd™###############################################################################################################
