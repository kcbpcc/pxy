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
bsma = check_index_status('^NSEBANK')

import sys
import traceback
import pandas as pd
import requests
import numpy as np
from login_get_kite import get_kite, remove_token
from cmbddfpxy import process_data  # Importing process_data function from cmbddfpxy module
from smapxy import check_index_status
from clorpxy import BRIGHT_YELLOW, BRIGHT_RED, BRIGHT_GREEN, RESET

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
            response.raise_for_status()  # Raise exception for non-200 status codes
            print("Telegram message sent successfully.")
    except requests.exceptions.RequestException as e:
        print(f"Failed to send Telegram message: {e}")

def place_order(tradingsymbol, quantity, transaction_type, order_type, product, broker):
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
def determine_target(bsma, key):
    if (bsma == "up" and "CE" in key) or (bsma == "down" and "PE" in key):
        return 10
    else:
        return 5
def exit_options(exe_opt_df_grouped, bsma, broker):
    try:
        for group_name, group_data in exe_opt_df_grouped:
            # Calculate target for each row in the group
            group_data['target'] = group_data.apply(
                lambda row: determine_target(bsma, row['key']),
                axis=1
            )
            
            for index, row in group_data.iterrows():
                if row['PL%'] > row['target']:
                    order_id = place_order(row['key'], row['qty'], 'SELL', 'MARKET', 'NRML', broker)
                    
                    if order_id:
                        message = f"🛬🛬🛬 👈👈👈 EXIT order placed for option {row['key']} successfully.\nPL: {row['PnL']}, PL%: {row['PL%']}%"
                        print(message)
                        send_telegram_message(message)
                    else:
                        print(f"Failed to place order for option {row['key']}.")

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

# Process data and handle exceptions
try:
    combined_df = process_data()
except Exception as e:
    print(f"Error processing data: {e}")
    traceback.print_exc()
    sys.exit(1)

# Calculate and manipulate dataframes
try:
    exe_opt_df = combined_df[combined_df['key'].str.contains('NFO:', case=False)].copy()
    exe_opt_df['key'] = exe_opt_df['key'].str.replace('NFO:', '') 
    exe_opt_df['PL%'] = (exe_opt_df['PnL'] / exe_opt_df['Invested']) * 100
    exe_opt_df['PL%'] = exe_opt_df['PL%'].fillna(0)
    exe_opt_df['target'] = exe_opt_df.apply(
        lambda row: 10 if ((bsma == 'up' and 'CE' in row['key']) or (bsma == 'down' and 'PE' in row['key'])) else 5,
        axis=1
    )
    exe_opt_df['strike'] = exe_opt_df['key'].str.replace(r'(PE|CE)$', '', regex=True)

    group_by_column = 'tradingsymbol'
    exe_opt_df_grouped = exe_opt_df.groupby(group_by_column)

    # Call exit_options with exe_opt_df_grouped and broker
    exit_options(exe_opt_df_grouped, broker)

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
    color_code_summary = BRIGHT_YELLOW
    summary_sentence = f"{color_code_summary}SUMMARY: CAP:{total_invested_all} P&L:{total_pl_all:5.0f} P&L%:{total_pl_percentage_all:3.0f}%{RESET}"
    summary_statement = summary_sentence

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

except Exception as e:
    print(f"Error: {e}")
    traceback.print_exc()

