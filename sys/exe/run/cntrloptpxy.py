import sys
import traceback
import pandas as pd
from login_get_kite import get_kite, remove_token
from cnstpxy import dir_path
from toolkit.logger import Logger
import csv
import os
import logging
from clorpxy import SILVER, UNDERLINE, RED, GREEN, YELLOW, RESET, BRIGHT_YELLOW, BRIGHT_RED, BRIGHT_GREEN, BOLD, GREY
import requests  
import numpy as np
############################################"PXY® PreciseXceleratedYield Pvt Ltd™############################################
bot_token = '6867988078:AAGNBJqs4Rf8MR4xPGoL1-PqDOYouPan7b0'
user_usernames = ('-4136531362',)  
def send_telegram_message(message):
    try:
        for username in user_usernames:
            url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
            payload = {
                'chat_id': username,
                'text': message
            }
            response = requests.post(url, data=payload)
            if response.status_code != 200:
                print(f"Failed to send Telegram message. Status code: {response.status_code}")
            else:
                print("Telegram message sent successfully.")
    except Exception as e:
        print(f"Error sending Telegram message: {e}")
############################################"PXY® PreciseXceleratedYield Pvt Ltd™############################################
def place_order(tradingsymbol, quantity, transaction_type, order_type, product):
    try:
        order_id = broker.order_place(
            tradingsymbol=tradingsymbol,
            quantity=quantity,
            exchange='NFO',
            transaction_type=transaction_type,
            order_type=order_type,
            product=product
        )
        print(f"Order placed successfully. Order ID: {order_id}")
        return order_id
    except Exception as e:
        print(f"Error placing order: {e}")
        return None
############################################"PXY® PreciseXceleratedYield Pvt Ltd™############################################
def exit_ce_options(key, pl_percentage, quantity, pnl):
    if key.endswith('CE') and pl_percentage >= 110 and quantity > 0:
        try:
            place_order(key, quantity, 'SELL', 'MARKET', 'NRML')  
            message = f"Exit order placed for {key} successfully.\nPL: {pnl}, PL%: {pl_percentage}%"
            print(message)
            send_telegram_message(message)
        except Exception as e:
            print(f"Error placing exit order for {key}: {e}")

try:
    sys.stdout = open('output.txt', 'w')
    broker = get_kite(api="bypass", sec_dir=dir_path)
except Exception as e:
    remove_token(dir_path)
    print(traceback.format_exc())
    logging.error(f"{str(e)} unable to get holdings")
    sys.exit(1)
finally:
    if sys.stdout != sys.__stdout__:
        sys.stdout.close()
        sys.stdout = sys.__stdout__
############################################"PXY® PreciseXceleratedYield Pvt Ltd™############################################

from cmbddfpxy import process_data
combined_df = process_data()
opt_df = combined_df[combined_df['key'].str.contains('NFO:', case=False)].copy()
opt_df['key'] = opt_df['key'].str.replace('NFO:', '') 
opt_df['PL%'] = (opt_df['PnL'] / opt_df['Invested']) * 100
opt_df['PL%'] = opt_df['PL%'].fillna(0)
opt_df['PL%'] = opt_df['PL%'].astype(int)  
opt_df = opt_df[['key', 'Invested', 'qty', 'PL%', 'PnL','pnl','product']]
total_invested = opt_df['Invested'].sum()
total_pl = opt_df['PnL'].sum()
total_pl_percentage = (total_pl / total_invested) * 100
total_real = opt_df.loc[opt_df['qty'] == 0, 'pnl'].sum()
############################################"PXY® PreciseXceleratedYield Pvt Ltd™############################################
print_df = opt_df.copy()
print_df['CP'] = opt_df['key'].apply(lambda x: '🟥' if x.endswith('PE') else ('🟩' if x.endswith('CE') else None))
print_df['key'] = print_df['key'].str.replace('NIFTY', 'N')
print_df['MN'] = np.where(print_df['product'] == 'MIS', '⌛', '🔢')
print_df = print_df[['MN', 'key', 'Invested', 'qty', 'PL%', 'PnL','pnl', 'CP']]
summary_sentence = f"CAP:{total_invested} | P&L:{total_pl} | P&L%:{total_pl_percentage:.2f}%{'🔴' if total_pl < 0 else '🟢'}"
print(f"{YELLOW}{summary_sentence.rjust(41)}{RESET}")

pd.set_option('display.max_colwidth', 42)
print_open_buy_df = print_df.loc[print_df['qty'] > 0, ['MN', 'key', 'Invested', 'qty', 'PL%', 'PnL', 'CP']]
print_close_df = print_df.loc[print_df['qty'] == 0, ['MN', 'key', 'Invested', 'qty', 'PL%', 'pnl', 'CP']]
print_open_sell_df = print_df.loc[print_df['qty'] < 0, ['MN', 'key', 'Invested', 'qty', 'PL%', 'PnL', 'CP']]
def print_formatted_df(df):
    formatted_lines = df.to_string(index=False, header=False, justify='left', col_space=1, line_width=42).split('\n')
    for line in formatted_lines:
        color_code = (GREEN if (float(line.split()[-2]) > 0) else (RED if (float(line.split()[-2]) < 0) else (YELLOW if (float(line.split()[-2]) == 0) else RESET))) if (len(line.split()) >= 2 and line.split()[-2].replace('.', '').isdigit()) else RESET
        print(color_code + (line[:-3] + line[-3:].rjust(3)).rjust(40) + RESET)
if not print_open_buy_df.empty:
    #print("Open Buy Trades:")
    print_formatted_df(print_open_buy_df)
if not print_close_df.empty:
    #print("Close Trades:")
    print_formatted_df(print_close_df)
    print(f"{GREEN if total_real >= 0 else RED}{'Options Profit Booked:':>38}{total_real}{RESET}")
if not print_open_sell_df.empty:
    #print("Open Sell Trades:")
    print_formatted_df(print_open_sell_df)
for index, row in opt_df.iterrows():
    exit_ce_options(row['key'], row['PL%'], row['qty'], row['PnL'])

