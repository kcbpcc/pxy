import pandas as pd
import numpy as np
import calendar
from datetime import datetime, timedelta
from lstdymnthexppxy import get_last_weekday_of_current_month
from clorpxy import BRIGHT_YELLOW, BRIGHT_GREEN, BRIGHT_RED, RESET
import subprocess

# Get the last Wednesday and Thursday of the current month
last_wednesday = get_last_weekday_of_current_month(calendar.WEDNESDAY)
last_thursday = get_last_weekday_of_current_month(calendar.THURSDAY)

# Read combined data from CSV
combined_df = pd.read_csv('pxycombined.csv')

# Calculate extras and total M2M for NIFTY and BANK
nifty_nfo_df = combined_df.loc[(combined_df['key'].str.contains('NFO:NIFTY'))]
if not nifty_nfo_df.empty:
    nextras = int(nifty_nfo_df.loc[nifty_nfo_df['sell_quantity'] > 0, 'unrealised'].sum()) + \
              ((-1) * int(nifty_nfo_df.loc[nifty_nfo_df['sell_quantity'] > 0, 'PnL'].sum()))
    ntotal_opt_m2m = nifty_nfo_df[nifty_nfo_df['quantity'] > 0]['m2m'].sum()
else:
    nextras = 0
    ntotal_opt_m2m = 0

bank_nfo_df = combined_df.loc[(combined_df['key'].str.contains('NFO:BANK'))]
if not bank_nfo_df.empty:
    bextras = int(bank_nfo_df.loc[bank_nfo_df['sell_quantity'] > 0, 'unrealised'].sum()) + \
              ((-1) * int(bank_nfo_df.loc[bank_nfo_df['sell_quantity'] > 0, 'PnL'].sum()))
    btotal_opt_m2m = bank_nfo_df[bank_nfo_df['quantity'] > 0]['m2m'].sum()
else:
    bextras = 0
    btotal_opt_m2m = 0

# Filter and process the DataFrame
opt_df = combined_df[combined_df['key'].str.contains('NFO:', case=False)].copy()
opt_df['key'] = opt_df['key'].str.replace('NFO:', '')
opt_df['PL%'] = (opt_df['PnL'] / opt_df['Invested']) * 100
opt_df['PL%'] = opt_df['PL%'].fillna(0)
opt_df['PL%'] = opt_df['PL%'].astype(int)
opt_df['m2m'] = opt_df['m2m'].astype(int)
opt_df = opt_df[['key', 'Invested', 'qty', 'PL%', 'PnL', 'pnl', 'product', 'm2m']]

total_invested = opt_df['Invested'].sum()
total_pl = opt_df['PnL'].sum()
total_opt_pnl = opt_df['m2m'].sum()
total_pl_percentage = (total_pl / total_invested) * 100 if total_invested != 0 else 0

# Create and process the print_df DataFrame
print_df = opt_df.copy()
print_df['CP'] = opt_df['key'].apply(lambda x: '🟠' if x.endswith('PE') else ('🟢' if x.endswith('CE') else None))
print_df['group'] = print_df['key'].str.extract(r'^(B|N)', expand=False)
print_df['key'] = print_df['key'].str.replace('BANKNIFTY24', 'B').str.replace('NIFTY24', 'N')
print_df['strike'] = print_df['key'].str.replace(r'(PE|CE)$', '', regex=True)
print_df['MN'] = np.where(print_df['product'] == 'MIS', '⌛', '🔢')
print_df = print_df[['MN', 'strike', 'Invested', 'qty', 'PL%', 'm2m', 'PnL', 'CP', 'group']]

# Summary calculations
summary_statement = ""
total_invested_all = print_df['Invested'].sum()
total_pl_all = (print_df['PnL'].sum() + (nextras + bextras))
total_pl_percentage_all = (total_pl_all / total_invested_all) * 100 if total_invested_all != 0 else 0
color_code_summary = BRIGHT_YELLOW

# Filter and group data
filtered_df = print_df[print_df['qty'] > 0]
grouped_df = filtered_df.groupby('group')

for group, data in grouped_df:
    total_invested_group = data['Invested'].sum()
    total_pl_group = data['PnL'].sum()
    total_pl_percentage_group = (total_pl_group / total_invested_group) * 100 if total_invested_group != 0 else 0
    pe_count = data['CP'].value_counts().get('🟠', 0)
    ce_count = data['CP'].value_counts().get('🟢', 0)

    pe_data = data[data['CP'] == '🟠']
    total_invested_pe = pe_data['Invested'].sum()
    total_pl_pe = pe_data['PnL'].sum()
    value_pe = total_invested_pe + total_pl_pe

    ce_data = data[data['CP'] == '🟢']
    total_invested_ce = ce_data['Invested'].sum()
    total_pl_ce = ce_data['PnL'].sum()
    value_ce = total_invested_ce + total_pl_ce

    if total_invested_group != 0:
        value_statement = f"{pe_count:02d} -🟥- {value_pe:06d}  ⚖   {value_ce:06d}  -🟩- {ce_count:02d}"
        summary_sentence = f"CAP:{total_invested_group} P&L:{total_pl_group:6.0f} P&L%:{total_pl_percentage_group:3.0f}%"
        color_code = BRIGHT_GREEN if total_pl_percentage_group > 0 else BRIGHT_RED
        print(data[data['qty'] > 0][['MN', 'strike', 'Invested', 'qty', 'PL%', 'PnL', 'CP']].to_string(header=False, index=False, col_space=[2, 10, 6, 3, 4, 7, 2]))

        if len(data) >= 2:
            formatted_output = f"{group}{last_wednesday if group == 'B' else last_thursday}⏰ {color_code}{summary_sentence}{RESET}".rjust(50)
            formatted_balance = f"{value_statement}{RESET}".center(44)
            print(formatted_output)
            print(formatted_balance)

subprocess.run(['python3', 'lstdymnthexppxy.py'])

# Define column width
column_width = 30
left_aligned_format = "{:<" + str(column_width) + "}"
right_aligned_format = "{:>" + str(column_width) + "}"
print("━" * 42)
print(summary_statement + "📊")

# Prepare output lines
output_lines = []

# Example values (replace these with your actual values or calculations)
nifty_profit = int(nextras)
nifty_loss = int(ntotal_opt_m2m)
bank_profit = int(bextras)
bank_loss = int(btotal_opt_m2m)

# Append formatted lines to output
output_lines.append(left_aligned_format.format(f"NIFTY-DL:{BRIGHT_RED if nifty_loss < 0 else BRIGHT_GREEN}{nifty_loss}{RESET}") +
                   right_aligned_format.format(f"NIFTY-DP:{BRIGHT_GREEN if nifty_profit > 0 else BRIGHT_RED}{nifty_profit}{RESET}"))

output_lines.append(left_aligned_format.format(f"BANK-DL:{BRIGHT_RED if bank_loss < 0 else BRIGHT_GREEN}{bank_loss}{RESET}") +
                   right_aligned_format.format(f"BANK-DP:{BRIGHT_GREEN if bank_profit > 0 else BRIGHT_RED}{bank_profit}{RESET}"))

# Join and print the formatted output
full_output = '\n'.join(output_lines)
print(full_output)
print("━" * 42)

