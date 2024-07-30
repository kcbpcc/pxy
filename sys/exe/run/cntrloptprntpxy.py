print("━" * 42)
import os
import argparse
import pandas as pd
import numpy as np
import calendar
from datetime import datetime
from expdaypxy import get_last_weekday_of_current_month
from predictpxy import predict_market_sentiment
from bpredictpxy import predict_bnk_sentiment
from mktpxy import get_market_check
mktpredict = predict_market_sentiment()
bmktpredict = predict_bnk_sentiment()
bonemincandlesequance, bmktpxy = get_market_check('^NSEBANK')
nonemincandlesequance, nmktpxy = get_market_check('^NSEI')
from prftpxy import process_data_total_profit
booked = process_data_total_profit()
from telsumrypxy import check_and_send_summary
from acvalpxy import get_current_acvalue, process_acvalue

try:
    from fundpxy import calculate_decision
    decision, optdecision, available_cash,live_balance, limit = calculate_decision()
except Exception as e:
    decision, optdecision, available_cash,live_balance, limit = "No", "No", 0, 0, 0

from clorpxy import SILVER, UNDERLINE, RED, GREEN, YELLOW, RESET, BRIGHT_YELLOW, BRIGHT_RED, BRIGHT_GREEN, BOLD, GREY

parser = argparse.ArgumentParser(description="Process some commands.")
parser.add_argument('command', nargs='?', choices=['l', 's'], default='s',
                    help="Command to run the program with. Defaults to 's' if not provided.")
args = parser.parse_args()

# Get the last Wednesday and Thursday of the current month
last_wednesday = get_last_weekday_of_current_month(calendar.WEDNESDAY)
last_thursday = get_last_weekday_of_current_month(calendar.THURSDAY)

# Read combined data from CSV
combined_df = pd.read_csv('pxycombined.csv')
total_ac_value = round(combined_df.loc[combined_df['qty'] > 0, 'value'].sum() / 100000, 2)
total_ac_run_pnl = round(combined_df.loc[combined_df['qty'] > 0, 'pnl'].sum() / 100000, 2)

# Define a helper function to calculate extras and M2M
import numpy as np
import pandas as pd

# Ensure df is defined and populated with your data
# Example: df = pd.read_csv('your_data.csv')

def calculate_extras_and_m2m(df):
    df_copy = df.copy()
    df_copy.loc[:, 'new_extras'] = np.where(
        df_copy['quantity'] == 0,
        df_copy['unrealised'],
        np.where(
            (df_copy['quantity'] > 0) & (df_copy['day_sell_quantity'] > 0),
            df_copy['unrealised'] - df_copy['PnL'],
            df_copy['unrealised']
        )
    )
    extras = df_copy['new_extras'].sum()
    total_m2m = df_copy[df_copy['quantity'] > 0]['m2m'].sum()
    return int(extras), total_m2m
    

# Calculate extras and total M2M for NIFTY and BANK
# Filter Nifty DataFrame with additional condition
nifty_df = combined_df[
    (combined_df['key'].str.lower().str.startswith('nfo:nifty')) &
    (combined_df['day_sell_quantity'] > 0)
]
nextras, ntotal_opt_m2m = calculate_extras_and_m2m(nifty_df)

# Filter Bank Nifty DataFrame with additional condition
bank_df = combined_df[
    (combined_df['key'].str.lower().str.startswith('nfo:banknifty')) &
    (combined_df['day_sell_quantity'] > 0)
]
bextras, btotal_opt_m2m = calculate_extras_and_m2m(bank_df)

# Filter and process the DataFrame
opt_df = combined_df[combined_df['key'].str.contains('NFO:', case=False)].copy()
opt_df['key'] = opt_df['key'].str.replace('NFO:', '', regex=False)
opt_df['PL%'] = ((opt_df['PnL'] / opt_df['Invested']) * 100).fillna(0).astype(int)
opt_df['m2m'] = opt_df['m2m'].astype(int)
opt_df = opt_df[['key', 'Invested', 'qty', 'PL%', 'PnL', 'pnl', 'product', 'm2m']]

total_invested = opt_df['Invested'].sum()
total_pl = opt_df['PnL'].sum()
total_opt_pnl = opt_df['m2m'].sum()
total_pl_percentage = (total_pl / total_invested) * 100 if total_invested != 0 else 0

# For calculating 'run_opnl'
run_opnl = combined_df[combined_df['exchange'] == 'NFO']['pnl'].sum()

# For calculating 'run_spnl'
run_spnl = combined_df[(combined_df['qty'] > 0) & (combined_df['exchange'].isin(['BSE', 'NSE']))]['pnl'].sum()

# Create and process the print_df DataFrame
print_df = opt_df.copy()
print_df['CP'] = print_df['key'].apply(lambda x: '🟠' if x.endswith('PE') else ('🟢' if x.endswith('CE') else None))
print_df['group'] = print_df['key'].str.extract(r'^(B|N)', expand=False)
print_df['key'] = print_df['key'].str.replace('BANKNIFTY24', 'B').str.replace('NIFTY24', 'N')
print_df['strike'] = print_df['key'].str.replace(r'(PE|CE)$', '', regex=True)
print_df['MN'] = np.where(print_df['product'] == 'MIS', '⌛', '🔢')
print_df = print_df[['MN', 'strike', 'Invested', 'qty', 'PL%', 'm2m', 'PnL', 'CP', 'group']]

# Summary calculations
total_invested_all = print_df['Invested'].sum()
total_pl_all = print_df['PnL'].sum() + nextras + bextras
total_pl_percentage_all = (total_pl_all / total_invested_all) * 100 if total_invested_all != 0 else 0

summary_statement = (
    f"{BRIGHT_YELLOW}SUMMARY-CAP:{total_invested_all:6.0f} P&L:{total_pl_all:7.0f} P&L%:{total_pl_percentage_all:3.0f}%{RESET}"
)

# Filter and group data
filtered_df = print_df.query('qty > 0')
grouped_df = filtered_df.groupby('group')

for group, data in grouped_df:
    total_invested_group = data['Invested'].sum()
    total_pl_group = data['PnL'].sum() + (nextras if group == 'N' else bextras if group == 'B' else 0)
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
    ce_pe_ratio = round((value_ce / value_pe), 2) if value_pe != 0 else 0

    if total_invested_group != 0:
        value_statement = f"  {pe_count:02d} -🟥- {value_pe:06d}  ⚖   {value_ce:06d}  -🟩- {ce_count:02d}"
        summary_sentence = f"CAP:{total_invested_group} P&L:{total_pl_group:6.0f} P&L%:{total_pl_percentage_group:3.0f}%"
        color_code = BRIGHT_GREEN if total_pl_percentage_group > 0 else BRIGHT_RED
        color_none = SILVER
        # Check the command and print the corresponding output
        if args.command == 'l':
            # Filter DataFrame with qty > 0
            filtered_data = data.query('qty > 0')[['MN', 'strike', 'Invested', 'qty', 'PL%', 'PnL', 'CP']]
            if not filtered_data.empty:
                print(filtered_data.to_string(header=False, index=False, col_space=[2, 10, 6, 3, 4, 7, 2]))
        elif args.command == 's':
            pass
            #filtered_data = data.query('qty > 0 and `PL%` > 0')[['MN', 'strike', 'Invested', 'qty', 'PL%', 'PnL', 'CP']]
            #if not filtered_data.empty:
                #print(filtered_data.to_string(header=False, index=False, col_space=[2, 10, 6, 3, 4, 7, 2]))
        if len(data) >= 2:
            formatted_output = f"{last_wednesday if group == 'B' else last_thursday}⏰ {color_none}{summary_sentence}{RESET}".rjust(50)
            formatted_balance = f"{value_statement}{RESET}".center(44)
            print(formatted_balance)            
            print(formatted_output)

    # Define ce_pe_ratio based on group
    if group == 'B':
        ratio_B = ce_pe_ratio
        #print(f"Group B CE/PE ratio: {ratio_B}")
    elif group == 'N':
        ratio_N = ce_pe_ratio
        #print(f"Group N CE/PE ratio: {ratio_N}")
    # Run the appropriate Python script based on the group value
    if group == 'N' and args.command == 's':
        os.system('python cndlpxy.py')
    elif group == 'B' and args.command == 's':
        os.system('python bcndlpxy.py')
###################################################################################"PXY® PreciseXceleratedYield Pvt Ltd™########################################################################################################################

acvalue = round(total_ac_value + (available_cash / 100000), 2)

from utcpxy import peak_time
peak = peak_time()
peak == "PREPEAK" and process_acvalue(acvalue)

print(f"{summary_statement}📊")

print("━" * 42)
column_width = 30
left_aligned_format = "{:<" + str(column_width) + "}"
right_aligned_format = "{:>" + str(column_width) + "}"

output_lines = []
nifty_profit = int(nextras)
nifty_loss = int(ntotal_opt_m2m)
bank_profit = int(bextras)
bank_loss = int(btotal_opt_m2m)
arrow_map = {"Buy": "↗", "Sell": "↘", "Bull": "↑", "Bear": "↓"}
hide = 0
cap = 17.82
real_pnl = round((total_ac_value + (available_cash / 100000)) - (cap + hide), 2)
all_Stocks_df = combined_df[
    (combined_df['qty'] > 0) &
    (combined_df['product'] == 'CNC') &
    (combined_df['source'] == 'holdings')
].copy()

all_Stocks_yworth = (all_Stocks_df['close'] * all_Stocks_df['qty']).sum().round(4)
all_Stocks_worth = (all_Stocks_df['ltp'] * all_Stocks_df['qty']).sum().round(4)
all_Stocks_worth_dpnl = all_Stocks_worth - all_Stocks_yworth
filtered_df = combined_df[(combined_df['product'] == 'CNC') &
                          (combined_df['qty'] > 0) &
                          (combined_df['PL%'] > 0)]
green_Stocks_profit_loss = filtered_df['PnL'].sum()
total_invested = filtered_df['Invested'].sum()
green_Stocks_capital_percentage = (green_Stocks_profit_loss / total_invested) * 100 if total_invested > 0 else 0

#output_lines.append(left_aligned_format.format(f"BANKNIFTY ━━ {BRIGHT_GREEN if bmktpredict == 'RISE' else BRIGHT_RED if bmktpredict == 'FALL' else BRIGHT_YELLOW}{bmktpredict} {arrow_map.get(bmktpxy, '')}{RESET}") +
                    #right_aligned_format.format(f"{BRIGHT_GREEN if mktpredict == 'RISE' else BRIGHT_RED if mktpredict == 'FALL' else BRIGHT_YELLOW}{arrow_map.get(nmktpxy, '')} {mktpredict}{RESET} ━━ NIFTYNDEX"))  

output_lines.append(
    left_aligned_format.format(f"Run-sPnL:{BRIGHT_RED if run_spnl < 0 else BRIGHT_GREEN}{round(run_spnl / 100000, 2)}{RESET}") +
    right_aligned_format.format(f"Real-PnL:{BRIGHT_GREEN if real_pnl > 0 else BRIGHT_RED}{real_pnl}{RESET}")
)

output_lines.append(left_aligned_format.format(f"Run-oPnL:{BRIGHT_GREEN if run_opnl > 0 else BRIGHT_RED}{str(round(run_opnl/100000, 2)).zfill(4)}{RESET}") +
                    right_aligned_format.format(f"Cash:{BRIGHT_GREEN if live_balance > 50000 else BRIGHT_YELLOW}{str(int(live_balance)).zfill(6)}{RESET}"))

output_lines.append(
    left_aligned_format.format(
        f"{'Capital'.zfill(7)}:{BRIGHT_YELLOW}{str(round(17.82, 2)).zfill(5)}"
        f"{BRIGHT_GREEN if nmktpxy in ['Bull', 'Buy'] else BRIGHT_RED}      {BOLD}{UNDERLINE}PXY{RESET}"
    ) +
    right_aligned_format.format(
        f"{BRIGHT_GREEN if nmktpxy in ['Bull'] else (BRIGHT_RED if nmktpxy in ['Bear'] else GREY)}"
        f"{BOLD}{UNDERLINE}®{RESET}{BRIGHT_YELLOW}{arrow_map.get(nmktpxy, '')}{RESET}       "
        f"{'Value'.zfill(5)}:{BRIGHT_YELLOW}{str(round(acvalue, 2)).zfill(5)}{RESET}"
    )
)

output_lines.append(left_aligned_format.format(
        f"Flush:{BRIGHT_GREEN if green_Stocks_profit_loss > 0 else BRIGHT_RED}{int(green_Stocks_profit_loss)}{RESET}") +
        right_aligned_format.format(
        f"Flush%:{BRIGHT_GREEN if green_Stocks_capital_percentage > 0 else BRIGHT_RED}{str(round(green_Stocks_capital_percentage, 2)).zfill(4)}%{RESET}"))
output_lines.append(left_aligned_format.format(
        f"HOLD-dPnL:{BRIGHT_GREEN if all_Stocks_worth_dpnl > 0 else BRIGHT_RED}{int(round(all_Stocks_worth_dpnl, 0))}{RESET}") +
        right_aligned_format.format(
        f"BOOKED:{GREEN if booked > 0 else RED}{str(int(booked)).zfill(5)}{RESET}"))

#output_lines.append(
    #left_aligned_format.format(f"B-Expiry:{GREY}{last_wednesday}{RESET}") +
    #right_aligned_format.format(f"N-Expiry:{GREY}{last_thursday}{RESET}")
#)
output_lines.append(
    left_aligned_format.format(f"BANK-DP:{BRIGHT_GREEN if bank_profit > 0 else BRIGHT_RED}{bank_profit}{RESET}") +
    right_aligned_format.format(f"NIFTY-DP:{BRIGHT_GREEN if nifty_profit > 0 else BRIGHT_RED}{nifty_profit}{RESET}")
)
output_lines.append(
    left_aligned_format.format(f"{BRIGHT_YELLOW}B━{ratio_B}/-/N━{ratio_N}{RESET}") +
    right_aligned_format.format(f"Total-PnL:{BRIGHT_GREEN if (nifty_profit + bank_profit +booked) > 0 else BRIGHT_RED}{nifty_profit + bank_profit + booked}{RESET}")
)

full_output = '\n'.join(output_lines)

print(full_output)
print("━" * 42)
summary = (
    f"---------PXY® Dash Board----------\n"
    f"    📈 A/C Run-PnL: {total_ac_run_pnl}\n"
    f"    🪙 Margin: {str(int(available_cash)).zfill(6)}\n"
    f"    💵 Cash: {str(int(live_balance)).zfill(6)}\n"
    f"    🏦 A/C Capital: {str(round(17.82, 2)).zfill(5)}\n"
    f"    💸 A/C Value: {str(round(total_ac_value + (available_cash / 100000), 2)).zfill(5)}\n"
    f"    📊 Holdings Day: {int(round(all_Stocks_worth_dpnl, 0))}\n"
    f"    📝 Stocks Day-PnL: {str(int(booked)).zfill(5)}\n"
    f"    🏧 Bank Day-Proft: {str(bank_profit).zfill(5)}\n"
    f"    🛺 Nifty Day-Proft: {str(nifty_profit).zfill(5)}\n"
    f"    ⚖️ B━{ratio_B} /🏋🏽/ N━{ratio_N}\n"
    f"    🎖️ A/C Real Total-PnL: {real_pnl}\n"
    f"    💰 Day Total-PnL: {str(nifty_profit + bank_profit + booked).zfill(5)}\n"
    f"                      \n"
    f"[---------PXY® Dash Board----------](https://console.zerodha.com/verified/783d6dad)\n"
)


# Function to send summary
check_and_send_summary(summary, 'bordpxy')
