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
from cmbddfpxy import process_data
from nftpxy import ha_nse_action, nse_power, Day_Change, Open_Change
from clorpxy import SILVER, UNDERLINE, RED, GREEN, YELLOW, RESET, BRIGHT_YELLOW, BRIGHT_RED, BRIGHT_GREEN, BOLD, GREY
from smapxy import check_index_status
bsma = check_index_status('^NSEBANK')
nsma = check_index_status('^NSEI')
#--------------------------------------------------- 🏛 🏛 PXY® PreciseXceleratedYield Pvt Ltd™ 🏛 ---------------------------------------------------
import numpy as np

# Filter and process the DataFrame
opt_df = combined_df[combined_df['key'].str.contains('NFO:', case=False)].copy()
opt_df['key'] = opt_df['key'].str.replace('NFO:', '')
opt_df['tgtoptsma'] = opt_df.apply(compute_tgtoptsma, axis=1)
opt_df['tgtoptsmadepth'] = opt_df.apply(compute_depth, axis=1)
opt_df['PL%'] = (opt_df['PnL'] / opt_df['Invested']) * 100
opt_df['PL%'] = opt_df['PL%'].fillna(0)
opt_df['PL%'] = opt_df['PL%'].astype(int)
opt_df['m2m'] = opt_df['m2m'].astype(int)
opt_df = opt_df[['key', 'Invested', 'qty', 'PL%', 'PnL', 'pnl', 'product', 'm2m','tgtoptsmadepth']]

total_invested = opt_df['Invested'].sum()
total_pl = opt_df['PnL'].sum()
total_opt_m2m = opt_df['m2m'].sum()
total_pl_percentage = (total_pl / total_invested) * 100 if total_invested != 0 else 0

# Create and process the print_df DataFrame
print_df = opt_df.copy()
print_df['CP'] = opt_df['key'].apply(lambda x: '🟥' if x.endswith('PE') else ('🟩' if x.endswith('CE') else None))
print_df['group'] = print_df['key'].str.extract(r'^(B|N)', expand=False)
print_df['key'] = print_df['key'].str.replace('BANKNIFTY24', 'B').str.replace('NIFTY24', 'N')
print_df['strike'] = print_df['key'].str.replace(r'(PE|CE)$', '', regex=True)
print_df['MN'] = np.where(print_df['product'] == 'MIS', '⌛', '🔢')
print_df = print_df[['MN', 'strike', 'Invested', 'qty', 'PL%', 'PnL', 'CP', 'group','tgtoptsmadepth']]

# Summary calculations
summary_statement = ""
total_invested_all = print_df['Invested'].sum()
total_pl_all = print_df['PnL'].sum()
total_pl_percentage_all = (total_pl_all / total_invested_all) * 100 if total_invested_all != 0 else 0
color_code_summary = BRIGHT_YELLOW
summary_sentence = f"{color_code_summary}SUMMARY-CAP:{total_invested_all:6.0f} P&L:{total_pl_all:7.0f} P&L%:{total_pl_percentage_all:3.0f}%{RESET}"
summary_statement = summary_sentence
print(summary_statement + "📊")

# Filter and group data
filtered_df = print_df[print_df['qty'] > 0]
grouped_df = filtered_df.groupby('group')

for group, data in grouped_df:
    total_invested_group = data['Invested'].sum()
    total_pl_group = data['PnL'].sum()
    total_pl_percentage_group = (total_pl_group / total_invested_group) * 100 if total_invested_group != 0 else 0
    
    if total_invested_group != 0:
        summary_sentence = f"CAP:{total_invested_group} P&L:{total_pl_group:6.0f} P&L%:{total_pl_percentage_group:3.0f}%"
        color_code = BRIGHT_GREEN if total_pl_percentage_group > 0 else BRIGHT_RED
        print(data[data['qty'] > 0][['MN', 'strike', 'Invested', 'qty','tgtoptsmadepth', 'PL%', 'PnL', 'CP']].to_string(header=False, index=False, col_space=[2, 10, 5, 3, 2, 3, 6,2]))
        
        if len(data) >= 2:
            formatted_output = f"{group}{color_code}{summary_sentence}{RESET}".rjust(51)
            print(formatted_output)

print("━" * 42)
