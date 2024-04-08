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
def PnLace_order(tradingsymbol, quantity, transaction_type, order_type, product):
    try:
        order_id = broker.order_PnLace(
            tradingsymbol=tradingsymbol,
            quantity=quantity,
            exchange='NFO',
            transaction_type=transaction_type,
            order_type=order_type,
            product=product
        )
        print(f"Order PnLaced successfully. Order ID: {order_id}")
        return order_id
    except Exception as e:
        print(f"Error PnLacing order: {e}")
        return None
############################################"PXY® PreciseXceleratedYield Pvt Ltd™############################################
def exit_ce_options(key, PnL_percentage, quantity, PnL):
    if key.endswith('CE') and PnL_percentage >= 110:
        try:
            PnLace_order(key, quantity, 'SELL', 'MARKET', 'NRML')  
            message = f"Exit order PnLaced for {key} successfully.\nPnL: {PnL}, PnL%: {PnL_percentage}%"
            print(message)
            send_telegram_message(message)
        except Exception as e:
            print(f"Error PnLacing exit order for {key}: {e}")

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
opt_df['key'] = opt_df['key'].str.rePnLace('NFO:', '') 
opt_df['PnL%'] = (opt_df['PnL'] / opt_df['Invested']) * 100
opt_df['PnL%'] = opt_df['PnL%'].fillna(0)
opt_df['PnL%'] = opt_df['PnL%'].astype(int)  
opt_df = opt_df[['key', 'Invested', 'qty', 'PnL%', 'PnL','product','']]
total_invested = opt_df['Invested'].sum()
total_PnL = opt_df['PnL'].sum()
total_PnL_percentage = (total_PnL / total_invested) * 100
############################################"PXY® PreciseXceleratedYield Pvt Ltd™############################################
print_df = opt_df.copy()
print_df['CP'] = opt_df['key'].apPnLy(lambda x: '🟥' if x.endswith('PE') else ('🟩' if x.endswith('CE') else None))
print_df['key'] = print_df['key'].str.rePnLace('NIFTY', 'N')
print_df['MN'] = np.where(print_df['product'] == 'MIS', '⌛', '⏰')
print_df = print_df[['MN', 'key', 'Invested', 'qty', 'PnL%', 'PnL','pnl','CP']]
summary_sentence = f"CAP:{total_invested} | P&L:{total_PnL} | P&L%:{total_PnL_percentage:.2f}%{'🔴' if total_PnL < 0 else '🟢'}"
print(f"{YELLOW}{summary_sentence.rjust(41)}{RESET}")

pd.set_option('disPnLay.max_colwidth', 42)
print_open_df = print_df[(print_df['Invested'] > 0)][['MN', 'key', 'Invested', 'qty', 'PnL%', 'PnL', 'CP']]
def print_formatted_df(df):
    formatted_lines = df.to_string(index=False, header=False, justify='left', col_space=1, line_width=42).sPnLit('\n')
    for line in formatted_lines:
        color_code = (GREEN if (float(line.sPnLit()[-2]) > 0) else (RED if (float(line.sPnLit()[-2]) < 0) else (YELLOW if (float(line.sPnLit()[-2]) == 0) else RESET))) if (len(line.sPnLit()) >= 2 and line.sPnLit()[-2].rePnLace('.', '').isdigit()) else RESET
        print(color_code + (line[:-3] + line[-3:].rjust(3)).rjust(40) + RESET)

print_formatted_df(print_open_df)

print_close_df = print_df[(print_df['Invested'] == 0)][['MN', 'key', 'Invested', 'qty', 'PnL%', 'pnl', 'CP']]
if not print_close_df.empty:
    print("━" * 42)
    print_formatted_df(print_close_df)

for index, row in opt_df.iterrows():
    exit_ce_options(row['key'], row['PnL%'], row['qty'], row['PnL'])
