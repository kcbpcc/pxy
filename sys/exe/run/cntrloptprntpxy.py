#print("━" * 42)
import yfinance as yf
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
from acvalpxy import process_acvalue, retrieve_acvalue
from smapxy import check_index_status
nsma = check_index_status('^NSEI')
bsma = check_index_status('^NSEBANK')
from nbsrikepxy import get_strike_prices
Bstrike, Nstrike = get_strike_prices()
from lncepepxy import format_investments 


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
cashround = round(live_balance / 100000, 2)
total_pl = opt_df['PnL'].sum()
total_opt_pnl = opt_df['m2m'].sum()
total_pl_percentage = (total_pl / total_invested) * 100 if total_invested != 0 else 0

# For calculating 'run_opnl'
run_opnl = combined_df[(combined_df['exchange'] == 'NFO')]['pnl'].sum()
CnC_tCap_rounded = round(combined_df.loc[(combined_df['product'] == 'CNC') & (combined_df['qty'] > 0), 'Invested'].sum() / 100000, 2)
m2m_opt = combined_df[(combined_df['exchange'] == 'NFO')]['m2m'].sum()

# For calculating 'run_spnl'
run_spnl = combined_df[(combined_df['qty'] > 0) & (combined_df['product'] == 'CNC') & (combined_df['source'] == 'holdings')]['pnl'].sum()
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
    f"{BRIGHT_YELLOW}CAP:{total_invested_all:6.0f} ━━━━ P&L:{total_pl_all:7.0f} ━━━━ P&L%:{total_pl_percentage_all:3.0f}%{RESET}"
)
#print("━" * 42)

#print(f"{summary_statement}")

# Filter and group data
filtered_df = print_df.query('qty > 0')
grouped_df = filtered_df.groupby('group')

###################################################################################"PXY® PreciseXceleratedYield Pvt Ltd™########################################################################################################################

acvalue = round(total_ac_value + (available_cash / 100000), 2)

from utcpxy import peak_time
peak = peak_time()

if peak == "PREPEAK":
    process_acvalue(acvalue)

acvalue = retrieve_acvalue()

#print(" " * 42)
column_width = 30
left_aligned_format = "{:<" + str(column_width) + "}"
right_aligned_format = "{:>" + str(column_width) + "}"

output_lines = []
nifty_profit = int(nextras)
nifty_loss = int(ntotal_opt_m2m)
bank_profit = int(bextras)
bank_loss = int(btotal_opt_m2m)
arrow_map = {"Buy": "⤴", "Sell": "⤵", "Bull": "⬆", "Bear": "⬇"}
hide = 0
cap = 17.82
real_pnl = round((acvalue + (available_cash / 100000)) - (cap), 2)
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

output_lines.append(left_aligned_format.format(f"C&C-tCap:{BRIGHT_YELLOW}{str(CnC_tCap_rounded).zfill(5)}{RESET}") +
                    right_aligned_format.format(f"C&C-tPnL:{BRIGHT_RED if run_spnl < 0 else BRIGHT_GREEN}{str(round(run_spnl / 100000, 2)).zfill(5)}{RESET}"))
output_lines.append(left_aligned_format.format(f"F&O-tCap:{BRIGHT_YELLOW}{str(round(total_invested_all / 100000, 2)).zfill(5)}{RESET}") +
                    right_aligned_format.format(f"F&O-tPnL:{BRIGHT_GREEN if run_opnl > 0 else BRIGHT_RED}{str(round(run_opnl / 100000, 2)).zfill(5)}{RESET}"))
output_lines.append(left_aligned_format.format(
        f"CashNow:{BRIGHT_GREEN if live_balance > 50000 else BRIGHT_YELLOW}{int(round(live_balance, 0)):06d}{RESET}") +
        right_aligned_format.format(
        f"Flush:{BRIGHT_GREEN if green_Stocks_capital_percentage > 0 else BRIGHT_RED}{str(round(green_Stocks_capital_percentage, 2)).zfill(4)}% {int(green_Stocks_profit_loss / 1000)}K{RESET}"))

output_lines.append(
    left_aligned_format.format(
        f"{'A/C-tCap'.zfill(7)}:{BRIGHT_YELLOW}{str(round(CnC_tCap_rounded + (total_invested_all / 100000), 2)).zfill(5)}"
        f"{BRIGHT_RED if mktpredict == 'FALL' else GREY if mktpredict == 'SIDE' else BRIGHT_GREEN}    {BOLD}PXY{RESET}"
    ) +
    right_aligned_format.format(
        f"{BRIGHT_GREEN if nmktpxy in ['Bull'] else (BRIGHT_RED if nmktpxy in ['Bear'] else GREY)}"
        f"{BOLD}®{RESET}{BRIGHT_YELLOW} {arrow_map.get(nmktpxy, '')}{RESET}    "
        f"{'A/C-tPnL'.zfill(5)}:{BRIGHT_GREEN}{str(round(CnC_tCap_rounded + (total_invested_all / 100000) + cashround - 17.8, 2)).zfill(5)}{RESET}"
    )
)

output_lines.append(
    left_aligned_format.format(
        f"C&C-dPnL:{BRIGHT_GREEN if all_Stocks_worth_dpnl > 0 else BRIGHT_RED}{str(int(round(all_Stocks_worth_dpnl, 0))).zfill(5)}{RESET}"
    ) + 
    right_aligned_format.format(
        f"F&O-dPnL:{BRIGHT_GREEN if m2m_opt > 0 else BRIGHT_RED}{str(int(m2m_opt)).zfill(5)}{RESET}"
    )
)



#output_lines.append(
    #left_aligned_format.format(f"B-Expiry:{GREY}{last_wednesday}{RESET}") +
    #right_aligned_format.format(f"N-Expiry:{GREY}{last_thursday}{RESET}")
#)
output_lines.append(
    left_aligned_format.format(f"BNK-bPnL:{BRIGHT_GREEN if bank_profit > 0 else BRIGHT_RED}{str(bank_profit).zfill(5)}{RESET}") +
    right_aligned_format.format(f"NFT-bPnL:{BRIGHT_GREEN if nifty_profit > 0 else BRIGHT_RED}{str(nifty_profit).zfill(5)}{RESET}")
)
output_lines.append(
    left_aligned_format.format(f"C&C-bPnL:{GREEN if booked > 0 else RED}{str(int(booked)).zfill(5)}{RESET}") +
    right_aligned_format.format(f"All-bPnL:{BRIGHT_GREEN if (nifty_profit + bank_profit + booked + hide) > 0 else BRIGHT_RED}{str(nifty_profit + bank_profit + booked + hide).zfill(5)}{RESET}"))

full_output = '\n'.join(output_lines)

print(full_output)

#print("━" * 42)

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
        Istrike = Nstrike if group == 'N' else Bstrike if group == 'B' else "Unknown"
        linecepepxy= format_investments(total_invested_pe, total_invested_ce)
        value_statement = f"  {pe_count:02d} -🟥- {total_invested_pe:06d}  {Istrike}   {total_invested_ce:06d}  -🟩- {ce_count:02d}"
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
            print(linecepepxy)            
            print(formatted_balance)            
            print(f"{UNDERLINE}{formatted_output}{RESET}") if args.command == 'l' else None
    # Define ce_pe_ratio based on group
    if group == 'B':
        ratio_B = ce_pe_ratio
        #print(f"Group B CE/PE ratio: {ratio_B}")
    elif group == 'N':
        ratio_N = ce_pe_ratio
        #print(f"Group N CE/PE ratio: {ratio_N}")
    # Run the appropriate Python script based on the group value
    if group == 'N' and args.command == 's':
        if nsma == "up":
            os.system('python cndlpxy.py')
            (lambda: print((BRIGHT_GREEN) + "ﮩ٨ﮩ٨ـﮩ٨ﮩ٨ـﮩ٨ـﮩﮩ٨ﮩ٨NIFTY٨ﮩ٨ـﮩ٨ـﮩﮩ٨ﮩ٨ـﮩ٨ﮩ٨ـﮩ" + RESET))()
        elif nsma == "down":
            (lambda: print((BRIGHT_RED) + "ﮩ٨ﮩ٨ـﮩ٨ﮩ٨ـﮩ٨ـﮩﮩ٨ﮩ٨NIFTY٨ﮩ٨ـﮩ٨ـﮩﮩ٨ﮩ٨ـﮩ٨ﮩ٨ـﮩ" + RESET))()
            os.system('python cndlpxy.py')
        else:
            (lambda: print((BRIGHT_YELLOW) + "ﮩ٨ﮩ٨ـﮩ٨ﮩ٨ـﮩ٨ـﮩﮩ٨ﮩ٨NIFTY٨ﮩ٨ـﮩ٨ـﮩﮩ٨ﮩ٨ـﮩ٨ﮩ٨ـﮩ" + RESET))()
    elif group == 'B' and args.command == 's':
        if bsma == "up":
            os.system('python bcndlpxy.py')
            (lambda: print((BRIGHT_GREEN) + "ﮩ٨ﮩ٨ـﮩ٨ﮩ٨ـﮩ٨ـﮩﮩ٨BANKNIFTY٨ﮩ٨ـﮩ٨ـﮩﮩ٨ﮩ٨ـﮩ٨ﮩ٨" + RESET))()
        elif bsma == "down":
            (lambda: print((BRIGHT_RED) + "ﮩ٨ﮩ٨ـﮩ٨ﮩ٨ـﮩ٨ـﮩﮩ٨BANKNIFTY٨ﮩ٨ـﮩ٨ـﮩﮩ٨ﮩ٨ـﮩ٨ﮩ٨" + RESET))()
            os.system('python bcndlpxy.py')
        else:
            (lambda: print((BRIGHT_YELLOW) + "ﮩ٨ﮩ٨ـﮩ٨ﮩ٨ـﮩ٨ـﮩﮩ٨BANKNIFTY٨ﮩ٨ـﮩ٨ـﮩﮩ٨ﮩ٨ـﮩ٨ﮩ٨" + RESET))()


summary = (
    f"---------PXY® Dash Board----------\n"
    f"      C&C-tCap    :{str(CnC_tCap_rounded).zfill(6)}\n"
    f"      C&C-tPnL    :{str(round(run_spnl / 100000, 2)).zfill(6)}\n"
    f"      F&O-tCap    :{str(round(total_invested_all / 100000, 2)).zfill(6)}\n"
    f"      F&O-tPnL    :{str(round(run_opnl / 100000, 2)).zfill(6)}\n"
    f"      A/C-tCap    :{str(round(CnC_tCap_rounded + (total_invested_all / 100000), 2)).zfill(6)}\n"
    f"      A/C-tPnL    :{str(round(CnC_tCap_rounded + (total_invested_all / 100000) - 17.8, 2)).zfill(6)}\n"
    f"      C&C-dPnL    :{str(int(round(all_Stocks_worth_dpnl, 0))).zfill(6)}\n"
    f"      F&O-dPnL    :{str(int(m2m_opt)).zfill(6)}\n"
    f"      C&C-bPnL    :{str(int(booked)).zfill(6)}\n"
    f"      BAK-bPnL    :{str(bank_profit).zfill(6)}\n"
    f"      NFT-bPnL    :{str(nifty_profit).zfill(6)}\n"
    f"     Cash-Left    :{str(int(round(live_balance, 0))).zfill(6)}\n"
    f"    Total-bPnL    :{str(nifty_profit + bank_profit + booked + hide).zfill(6)}\n"
    f"                      \n"
    f"[---------PXY® Dash Board----------](https://console.zerodha.com/verified/72e03b58)\n"
)


if peak == "PEAKSTAR": check_and_send_summary(summary, 'bordpxy')

