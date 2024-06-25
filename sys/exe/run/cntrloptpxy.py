import sys
import traceback
import subprocess
import pandas as pd
from login_get_kite import get_kite, remove_token
from cnstpxy import dir_path
import csv
import os
import logging
import requests
import numpy as np
from timetgtpxy import timetgt
from nftpxy import ha_nse_action, nse_power, Day_Change, Open_Change
from clorpxy import SILVER, UNDERLINE, RED, GREEN, YELLOW, RESET, BRIGHT_YELLOW, BRIGHT_RED, BRIGHT_GREEN, BOLD, GREY
from smapxy import check_index_status

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

def exit_options(exe_opt_df):
    try:
        for index, row in exe_opt_df.iterrows():
            total_invested = row['Invested']
            total_pl = row['PnL']
            total_pl_percentage = (total_pl / total_invested) * 100 if total_invested != 0 else 0
            tgtoptsma = row['tgtoptsma']
            
            if total_pl_percentage > tgtoptsma:
                place_order(row['key'], row['qty'], 'SELL', 'MARKET', 'NRML')
                
                message = f"🛬🛬🛬 👈👈👈 EXIT order placed for option with key {row['key']} successfully.\nPL: {total_pl}, PL%: {total_pl_percentage}%, Target PL%: {tgtoptsma}%"
                print(message)
                send_telegram_message(message)
                
    except Exception as e:
        print(f"Error placing exit order: {e}")

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

import pandas as pd
from cmbddfpxy import process_data

combined_df = process_data()
exe_opt_df = combined_df[combined_df['key'].str.contains('NFO:', case=False)].copy()
exe_opt_df['key'] = exe_opt_df['key'].str.replace('NFO:', '') 
exe_opt_df['PL%'] = (exe_opt_df['PnL'] / exe_opt_df['Invested']) * 100
exe_opt_df['PL%'] = exe_opt_df['PL%'].fillna(0)

# Define the 'strike' column
exe_opt_df['strike'] = exe_opt_df['key'].str.replace(r'(PE|CE)$', '', regex=True)

# Grouping by 'strike / 'tradingsymbol' column dynamic
from utcpxy import peak_time
peak = peak_time()
group_by_column = 'tradingsymbol' if peak == 'NONPEAK' else 'strike'
exe_opt_df = exe_opt_df.groupby(group_by_column)

def compute_tgtoptsma(row):
    if (row['bsma'] == "up" and "CE" in row['key']) or (row['bsma'] == "down" and "PE" in row['key']):
        return 10
    else:
        return 5

# Apply the function to each row and create a new column 'tgtoptsma'
exe_opt_df['tgtoptsma'] = exe_opt_df.apply(compute_tgtoptsma, axis=1)

# Call exit_options with exe_opt_df
exit_options(exe_opt_df)

opt_df = combined_df[combined_df['key'].str.contains('NFO:', case=False)].copy()
opt_df['key'] = opt_df['key'].str.replace('NFO:', '') 
opt_df['PL%'] = (opt_df['PnL'] / opt_df['Invested']) * 100
opt_df['PL%'] = opt_df['PL%'].fillna(0)
opt_df['PL%'] = opt_df['PL%'].astype(int) 
opt_df['m2m'] = opt_df['m2m'].astype(int)
opt_df = opt_df[['key', 'Invested', 'qty', 'PL%', 'PnL','pnl','product','m2m']]

total_invested = opt_df['Invested'].sum()
total_pl = opt_df['PnL'].sum()
total_opt_m2m = opt_df['m2m'].sum()
total_pl_percentage = (total_pl / total_invested) * 100 if total_invested != 0 else 0

# Grouping by 'strike' column
print_df = opt_df.copy()
print_df['CP'] = opt_df['key'].apply(lambda x: '🟥' if x.endswith('PE') else ('🟩' if x.endswith('CE') else None))
print_df['key'] = print_df['key'].str.replace('BANKNIFTY24', 'B').str.replace('NIFTY24', 'N')
print_df['strike'] = print_df['key'].str.replace(r'(PE|CE)$', '', regex=True)
print_df['MN'] = np.where(print_df['product'] == 'MIS', '⌛', '🔢')
print_df = print_df[['MN','strike','Invested', 'qty', 'PL%', 'PnL','CP']]

summary_statement = ""
total_invested_all = print_df['Invested'].sum()
total_pl_all = print_df['PnL'].sum()
total_pl_percentage_all = (total_pl_all / total_invested_all) * 100 if total_invested_all != 0 else 0
color_code_summary = BRIGHT_GREEN if total_pl_percentage_all > 0 else BRIGHT_RED
summary_sentence = f"{color_code_summary}SUMMARY: CAP:{total_invested_all} P&L:{total_pl_all:5.0f} P&L%:{total_pl_percentage_all:3.0f}%{RESET}"
summary_statement = summary_sentence
subprocess.run(['python3', 'bcndlpxy.py'])
subprocess.run(['python3', 'bniftychartpxy.py'])
bsma = check_index_status('^NSEBANK')
subprocess.run(['python3', 'bdaypxy.py']) 
print((GREEN if bsma == "up" else RED if bsma == "down" else YELLOW) + "ﮩ٨ﮩ٨ـﮩ٨ﮩ٨ـﮩ٨ـﮩﮩ٨ﮩ٨ـﮩ٨ﮩ٨ـﮩ٨ـﮩﮩ٨ﮩ٨ـﮩ٨ﮩ٨ـﮩ٨ـﮩ" + RESET)
grouped_df = print_df.groupby('strike')
for group, data in grouped_df:
    total_invested_group = data['Invested'].sum()
    total_pl_group = data['PnL'].sum()
    total_pl_percentage_group = (total_pl_group / total_invested_group) * 100 if total_invested_group != 0 else 0
    if total_invested_group != 0:  # Check if capital is not zero
        summary_sentence = f"CAP:{total_invested_group} P&L:{total_pl_group:6.0f} P&L%:{total_pl_percentage_group:3.0f}%"
        color_code = BRIGHT_GREEN if total_pl_percentage_group > 0 else BRIGHT_RED
        print(data[data['qty'] > 0][['MN', 'strike', 'Invested', 'qty', 'PL%', 'PnL', 'CP']].to_string(header=False, index=False, col_space=[2, 11, 5, 3, 3, 6, 4]))
        if len(data) >= 2:  # Check if group has two or more entries
            print(f"{group} {color_code}{summary_sentence}{RESET}")  # No need for .rjust here
print("━" * 42)
print(summary_statement +"📊" )
subprocess.run(['python3', 'cndlpxy.py'])
