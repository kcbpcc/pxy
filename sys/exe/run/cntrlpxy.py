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
def get_open_order_status(symbol):
    try:
        orders = broker.kite.orders()
        for order in orders:
            if order['status'] == 'OPEN' and order['tradingsymbol'] == symbol:
                return "YES"  
    except Exception as e:
        remove_token(dir_path)
        logging.error(f"{str(e)} unable to get orders")
        sys.exit(1)
    return "NO"  
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
                with open(csv_file_path, 'a', newline='') as csvfile:
                    csvwriter = csv.writer(csvfile)
                    csvwriter.writerow(row.tolist())  
                    try:
                        import telegram
                        import asyncio
                        columns_to_drop = ['smb_power', 'oPL%', 'm2m', '_pstp', 'qty', 'close', 'open', 'high', 'low', 'm2m', 'dPL%', 'pxy','yxp']
                        for column in columns_to_drop:
                            if column in row:
                                del row[column]
                        message_text = f"{str(row):>10} \nhttps://www.tradingview.com/chart/?symbol={key}\nBooked profit until now: {result}"
                        bot_token = '6867988078:AAGNBJqs4Rf8MR4xPGoL1-PqDOYouPan7b0'
                        user_usernames = ('-4136531362') 
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
###########################################################################################################################################################################################################
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
                try:
                    message_text = f"{row['ltp']} \nhttps://www.tradingview.com/chart/?symbol={exchsym[1]}"
                    bot_token = '6924826872:AAHTiMaXmjyYbGsCFhdZlRRXkyfZTpsKPug'
                    user_id = '-4135910842' 
                    async def send_telegram_message(message_text):
                        bot = telegram.Bot(token=bot_token)
                        await bot.send_message(chat_id=user_id, text=message_text)
                    asyncio.run(send_telegram_message(message_text))
                except Exception as e:
                    print(f"Error sending message to Telegram: {e}")
                return exchsym[1], remaining_cash 
            return True
        else:
            logging.error("Order placement failed")
    except Exception as e:
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
    logging.debug("Are we having any holdings to check")
    holdings_response = broker.kite.holdings()
    positions_response = broker.kite.positions()['net']
    holdings_df = get_holdingsinfo(holdings_response, broker)
    positions_df = get_positionsinfo(positions_response, broker)
    ###########################################################################################################################################################################################################
    try:
        response = broker.kite.margins()
        available_cash = response["equity"]["available"]["live_balance"]
    except Exception as e:
        print(f"An error occurred: {e}")
        available_cash = 0
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
    combined_df['oPL%'] = combined_df.apply(lambda row: (((row['ltp'] - row['open']) / row['open']) * 100) if row['open'] != 0 else 1, axis=1)
    combined_df['m2m'] = combined_df['m2m'].map(lambda x: dct.get(x, {}).get('m2m', 0))
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
            return None  
    from smapxy import check_index_status
    SMAfty = check_index_status('^NSEI')
###########################################################################################################################################################################################################
    from depthpxy import calculate_consecutive_candles
    cedepth, pedepth = calculate_consecutive_candles('^NSEI')
    combined_df['otPL%'] = (3 + combined_df.apply(lambda row: pedepth * 0.5 if row['key'].endswith('PE') else cedepth * 0.5  if row['key'].endswith('CE') else None, axis=1))
    combined_df['fPL%'] = combined_df['smb_power'].apply(lambda x: round(np.exp(np.clip(((x + nse_power) / 2), -threshold, threshold)), 2))
    combined_df['tPL%'] = np.round(np.maximum(combined_df['fPL%'], np.maximum(1.4, np.round(np.exp(np.clip(((combined_df['fPL%'] + nse_power) / 2), -threshold, threshold)), 2)) * nse_factor), 2)
    combined_df['tPL%'] = np.where(SMAfty == 'up', np.maximum(1 * combined_df['tPL%'], 1.4), np.where(SMAfty == 'down', np.maximum(combined_df['tPL%'] * 0.5, 1.4), combined_df['tPL%']))
###########################################################################################################################################################################################################
    combined_df['Invested'] = (combined_df['qty'] * combined_df['average_price']).round(0).astype(int)
    combined_df['value'] = combined_df['qty'] * combined_df['ltp']
    combined_df['value_H'] = combined_df['qty'] * combined_df['high']
    combined_df['PnL'] = (combined_df['value'] - combined_df['Invested']).astype(int)
    combined_df['PnL_H'] = combined_df['value_H'] - combined_df['Invested']
    combined_df['PL%'] = ((combined_df['PnL'] / combined_df['Invested']) * 100).round(2)
    combined_df['PL%_H'] = (combined_df['PnL_H'] / combined_df['Invested']) * 100
    combined_df['Yvalue'] = combined_df['qty'] * combined_df['close']
    combined_df['dPnL'] = combined_df['value'] - combined_df['Yvalue']
    combined_df['dPL%'] = (combined_df['dPnL'] / combined_df['Yvalue']) * 100
###########################################################################################################################################################################################################    
    import pandas as pd
    numeric_columns = ['fPL%','tPL%','smb_power','oPL%','otPL%','qty', 'average_price', 'Invested','Yvalue', 'ltp','close', 'open', 'high', 'low','value', 'PnL', 'PL%', 'm2m', 'dPnL', 'dPL%']
    combined_df[numeric_columns] = combined_df[numeric_columns].round(2)
    filtered_df = combined_df[((combined_df['product'].isin(['NRML', 'MIS'])) | ((combined_df['product'] == 'CNC') & (combined_df['qty'] > 0)))]
    combined_df_positive_qty = combined_df[(combined_df['qty'] > 0) & (combined_df['source'] == 'holdings')]
    filtered_df['PL%'] = filtered_df['PL%'].fillna(0)
    filtered_df['PL%'] = filtered_df['PL%'].astype(int)
    total_PnL = round(combined_df_positive_qty['PnL'].sum())
    total_PnL_percentage = (total_PnL / combined_df_positive_qty['Invested'].sum()) * 100 if combined_df_positive_qty['Invested'].sum() != 0 else 0
    stocks_buy_df = combined_df.loc[(combined_df['product'] == "CNC") & (combined_df['qty'] > 0) & (combined_df['source'] == "positions")]
    total_PnL_stocks_buy = round(stocks_buy_df['PnL'].sum()) if not stocks_buy_df.empty else 0
    options_buy_df = combined_df.loc[(combined_df['product'] == "NRML")]
    total_PnL_options_buy = round(options_buy_df['PnL'].sum()) if not options_buy_df.empty else 0
    total_invested__nrml = options_buy_df['Invested'].sum() if not options_buy_df.empty else 0
    options_percentage_return = round((total_PnL_options_buy / total_invested__nrml) * 100, 0) if total_invested__nrml != 0 else 0
    total_dPnL = round(combined_df_positive_qty['dPnL'].sum())
    total_dPnL_percentage = (total_dPnL / combined_df_positive_qty['Invested'].sum()) * 100 if combined_df_positive_qty['Invested'].sum() != 0 else 0
###########################################################################################################################################################################################################
    from smapxy import check_index_status
    nsma = check_index_status("^NSEI")
    print("━" * 42)
    from dshpxy import get_holdingsinfo
    total_nfom2m, all_Stocks_count, red_Stocks_count, green_Stocks_count, all_Stocks_capital_lacks, all_Stocks_worth_lacks, zero_qty_count, green_Stocks_profit_loss, green_Stocks_capital_rercentage,nrmlall_Stocks_count ,nrmlall_Stocks_capital ,nrmlall_Stocks_worth ,nrmlall_Stocks_profit_loss = get_holdingsinfo(combined_df)    
    from bordpxy import printbord
    printbord(total_nfom2m, optpxy, Day_Change, result, total_PnL_percentage, total_dPnL, total_PnL, total_dPnL_percentage,
             result_nrml, total_PnL_stocks_buy, total_PnL_options_buy, available_cash,
             nse_action, nse_power,all_Stocks_count, red_Stocks_count,green_Stocks_count,all_Stocks_capital_lacks,all_Stocks_worth_lacks, zero_qty_count, green_Stocks_profit_loss, green_Stocks_capital_rercentage, mktpxy,nrmlall_Stocks_count ,nrmlall_Stocks_capital ,nrmlall_Stocks_worth ,nrmlall_Stocks_profit_loss, nsma)
###########################################################################################################################################################################################################
    import pandas as pd
    from tabulate import tabulate
    lstchk_file = "fileHPdf.csv"
    combined_df.to_csv(lstchk_file, index=False)
    pxy_df = filtered_df.copy()[['fPL%','tPL%','smb_power','oPL%','otPL%','Invested','source','product', 'qty','average_price', 'close', 'ltp', 'open', 'high','low','key','dPL%','PnL', 'm2m', 'PL%']]
    pxy_df['avg'] = filtered_df['average_price']
    EXE_df = pxy_df[['tPL%','fPL%','smb_power','oPL%','otPL%','Invested','qty', 'avg', 'close', 'ltp', 'open', 'high', 'low', 'm2m', 'dPL%','product', 'source', 'key', 'PL%', 'PnL']]    
    PRINT_df = pxy_df[pxy_df['qty'] > 0][['source', 'product', 'key', 'tPL%', 'PL%', 'PnL', 'smb_power']]
    PRINT_df = PRINT_df.rename(columns={'source': 'HP', 'product': '_CM', 'smb_power': 'TR','key': 'key','dPL%': 'dPL%'})
    PRINT_df['HP'] = PRINT_df['HP'].replace({'holdings': '📌', 'positions': '🎯'})
    PRINT_df['_CM'] = PRINT_df['_CM'].replace({'CNC': '🧰', 'MIS': '⌛','NRML': '💸'}) 
    PRINT_df['TR'] = PRINT_df['TR'].apply(lambda TR: '⚪' if TR > 0.8 else ('🟢' if 0.5 < TR <= 0.8 else ('🟠' if 0.3 < TR <= 0.5 else ('🔴' if TR <= 0.3 else TR))))
    PRINT_df['key'] = PRINT_df['key'].str.replace(r'BSE:|NSE:', '', regex=True)
###########################################################################################################################################################################################################    
    print("━" * 42)
    import pandas as pd
    PRINT_df_sorted = PRINT_df.copy()
    PRINT_df_sorted['TR'] = PRINT_df_sorted['TR'].apply(lambda TR: TR[:2] if isinstance(TR, str) else TR)
    PRINT_df_sorted['key'] = PRINT_df_sorted['key'].str.replace(r'(BSE:|NSE:|NFO:)', '', regex=True).str[:20].str.ljust(20, ' ')
    PRINT_df_sorted = PRINT_df_sorted.sort_values(by='PL%', ascending=True)
    pd.set_option('display.max_colwidth', 1)
    PRINT_df_sorted_display = PRINT_df_sorted.copy()
    stocks_filtered_df = PRINT_df_sorted_display[(PRINT_df_sorted_display['PL%'] > 0 ) & (PRINT_df_sorted_display['_CM'] == '🧰')]
    options_filtered_df = pxy_df.loc[pxy_df['key'].str.startswith('NFO'), ['product','Invested','key', 'tPL%','otPL%', 'PL%', 'PnL', 'qty', 'smb_power']]
    options_filtered_df['otPL%'] = options_filtered_df['otPL%'].round(2)
    options_filtered_df['key'] = options_filtered_df['key'].str.replace('NFO:', '')
###########################################################################################################################################################################################################   
    from mktpxy import get_market_check
    importlib.reload(sys.modules['mktpxy'])
    onemincandlesequance, mktpxy = get_market_check('^NSEI')
    csv_file_path = "filePnL.csv"
    csv_file_path_nrml = 'filePnL_nrml.csv'
    selected_rows = []
    if nse_power < 1:
        try:
            for index, row in EXE_df.iterrows():
                excluded_keys = set(pd.read_csv("filePnL.csv", header=None).iloc[:, -3])
                key = row['key']
                symbol_in_order = row['key'].split(":")[1]
                if (
                    row['key'] not in excluded_keys and
                    row['open'] > 0 and
                    row['high'] > 0 and
                    row['low'] > 0 and
                    row['close'] > 0 and
                    row['ltp'] != 0
                ):
                    if (
                        (row['qty'] > 0 and
                         row['avg'] != 0 and
                         nse_power < 0.9 and
                         row['product'] == 'CNC' and
                         row['PL%'] > 1.4) and
                        (
                            (row['PL%'] > row['tPL%'])
                        )
                    ):
                        try:
                            is_placed = stocks_sell_order_place(key, row) if get_open_order_status(symbol_in_order) == "NO" else False
                            if is_placed:
                                print(row)
                        except InputException as e:
                            print(f"An error occurred while placing an order for key {key}: {e}")
                        except Exception as e:
                            print(f"An unexpected error occurred while placing an order for key {key}: {e}")
                    elif (
                        (row['qty'] > 0 and
                         row['avg'] != 0 and
                         available_cash > 20000 and
                         nse_power < 0.1 and
                         mktpxy in ['Buy', 'Bull'] and
                         row['PL%'] < -74)
                    ):
                        try:
                            is_placed = stocks_avg_order_place(key, row) if get_open_order_status(symbol_in_order) == "NO" else False
                            if is_placed:
                                print(row['key'])
                        except InputException as e:
                            print(f"An error occurred while placing an order for key {key}: {e}")
                        except Exception as e:
                            print(f"An unexpected error occurred while placing an order for key {key}: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
###########################################################################################################################################################################################################
    if not stocks_filtered_df.empty:
        print(stocks_filtered_df.to_string(index=False, justify='left', col_space=-0, header=False))
    else:
        print(YELLOW +".............no stocks reached target yet."+ RESET)
    print("━" * 42)
###########################################################################################################################################################################################################
    if not options_filtered_df.empty:
        filtered_df = options_filtered_df.copy()
        if not filtered_df.empty:
            filtered_df.loc[:, 'option_power'] = filtered_df['smb_power'].apply(lambda smb_power: '⚪' if smb_power > 0.8 else ('🟢' if 0.5 < smb_power <= 0.8 else ('🟠' if 0.3 < smb_power <= 0.5 else ('🔴' if smb_power <= 0.3 else smb_power))))
            import pandas as pd
            import numpy as np
            filtered_df['key'] = filtered_df['key'].str.replace('NIFTY', 'N')
            filtered_df.loc[:, 'PL%'] = filtered_df['PL%'].astype(int)
            filtered_df.loc[filtered_df['key'].str.endswith('CE'), 'key'] += ' 🟥'
            filtered_df.loc[filtered_df['key'].str.endswith('PE'), 'key'] += ' 🟩'
            filtered_df = filtered_df.sort_values(by='PL%')
            for index, row in filtered_df.iterrows():
                if row['product'] == 'MIS':
                    filtered_df.at[index, 'product'] = '⌛'
                elif row['product'] == 'NRML':
                    filtered_df.at[index, 'product'] = '⏰'
            formatted_lines = filtered_df[['product', 'Invested', 'key', 'qty', 'PL%','m2m', 'PnL']].to_string(index=False, header=False).split('\n')
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
                    else:
                        color_code = RESET
                else:
                    color_code = RESET
                print(color_code + (line[:-3] + line[-3:].rjust(3)) + RESET)
        else:
            print(YELLOW +"..............no options yet in the swing."+ RESET)
    else:
        print("mktpxy: " + YELLOW + "options not activated" + RESET + ", let's wait!")
###########################################################################################################################################################################################################
except Exception as e:
    remove_token(dir_path)
    print(traceback.format_exc())
    logging.error(f"{str(e)} in the main loop")
