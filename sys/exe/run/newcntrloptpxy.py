import sys
import traceback
import pandas as pd
import requests
import logging
from login_get_kite import get_kite, remove_token
from cnstpxy import dir_path
from cmbddfpxy import process_data
from smapxy import check_index_status
from utcpxy import peak_time
from depthpxy import calculate_consecutive_candles
from mktpxy import get_market_check
from predictpxy import predict_market_sentiment
from bpredictpxy import predict_bnk_sentiment
from clorpxy import SILVER, UNDERLINE, RED, GREEN, YELLOW, RESET, BRIGHT_YELLOW, BRIGHT_RED, BRIGHT_GREEN, BOLD, GREY
from ordlmtoptpxy import place_sell_limit_orders
from ordextoptpxy import exit_position

mktpredict = predict_market_sentiment()
bmktpredict = predict_bnk_sentiment()
bonemincandlesequance, bmktpxy = get_market_check('^NSEBANK')
nonemincandlesequance, nmktpxy = get_market_check('^NSEI')

bsma = check_index_status('^NSEBANK')
nsma = check_index_status('^NSEI')
arrow_map = {"Buy": "⤴", "Sell": "⤵", "Bull": "⬆", "Bear": "⬇"}
peak = peak_time()

column_width = 30
left_aligned_format = "{:<" + str(column_width) + "}"
right_aligned_format = "{:>" + str(column_width) + "}"
output_lines = []
output_lines.append(left_aligned_format.format(f"BNK ━━━━━━> {BRIGHT_GREEN if bmktpredict == 'RISE' else BRIGHT_RED if bmktpredict == 'FALL' else BRIGHT_YELLOW}{bmktpredict} {arrow_map.get(bmktpxy, '')}{RESET}") +
                    right_aligned_format.format(f"{BRIGHT_GREEN if mktpredict == 'RISE' else BRIGHT_RED if mktpredict == 'FALL' else BRIGHT_YELLOW}{arrow_map.get(nmktpxy, '')} {mktpredict}{RESET} <━━━━━━ NFT"))
full_output = '\n'.join(output_lines)
print(full_output)

bot_token = '7141714085:AAHlyEzszCy9N-L6wO1zSAkRwGdl0VTQCFI'
user_usernames = ('-4282665161',)

def send_telegram_message(message):
    try:
        for username in user_usernames:
            url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
            payload = {'chat_id': username, 'text': message}
            response = requests.post(url, data=payload)
            if response.status_code != 200:
                print(f"Failed to send Telegram message. Status code: {response.status_code}")
            else:
                print("Telegram message sent successfully.")
    except Exception as e:
        print(f"Error sending Telegram message: {e}")

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

combined_df = process_data()
exe_opt_df = combined_df[combined_df['key'].str.contains('NFO:', case=False)].copy()
exe_opt_df['key'] = exe_opt_df['key'].str.replace('NFO:', '') 
exe_opt_df['PL%'] = (exe_opt_df['PnL'] / exe_opt_df['Invested']) * 100
exe_opt_df['PL%'] = exe_opt_df['PL%'].fillna(0)

exe_opt_df['strike'] = exe_opt_df['key'].str.replace(r'(PE|CE)$', '', regex=True)

def compute_tgtoptsma(row):
    global bsma
    global nsma
    
    key = row['key']
    
    if (bsma == "up" and key.startswith("BANK") and "CE" in key) or (bsma == "down" and key.startswith("BANK") and "PE" in key):
        return 7
    elif (nsma == "up" and key.startswith("NIFTY") and "CE" in key) or (nsma == "down" and key.startswith("NIFTY") and "PE" in key):
        return 7
    else:
        return 5

exe_opt_df['tgtoptsma'] = exe_opt_df.apply(compute_tgtoptsma, axis=1)

bcedepth, bpedepth = calculate_consecutive_candles("^NSEBANK")
ncedepth, npedepth = calculate_consecutive_candles("^NSEI")
from vixpxy import get_vixpxy
n_vix, b_vix = get_vixpxy()
nvix = n_vix / 2
bvix = b_vix / 2

def compute_depth(row):
    try:
        global bcedepth, bpedepth, ncedepth, npedepth, bvix, nvix
        
        if "CE" in row['key'] and row['key'].startswith("BANK"):
            if bcedepth > 1:
                return max(row['tgtoptsma'], (bvix + 9 - bcedepth))
            else:
                return 5
        elif "PE" in row['key'] and row['key'].startswith("BANK"):
            if bpedepth > 1:
                return max(row['tgtoptsma'], (bvix + 9 - bpedepth))
            else:
                return 5
        elif "CE" in row['key'] and row['key'].startswith("NIFTY"):
            if ncedepth > 1:
                return max(row['tgtoptsma'], (nvix + 9 - ncedepth))
            else:
                return 5
        elif "PE" in row['key'] and row['key'].startswith("NIFTY"):
            if npedepth > 1:
                return max(row['tgtoptsma'], (nvix + 9 - npedepth))
            else:
                return 5
        else:
            return 5
    except Exception as e:
        return 5

exe_opt_df['tgtoptsmadepth'] = exe_opt_df.apply(compute_depth, axis=1)

if peak != 'PEAKSTART':
    exit_position(exe_opt_df, broker)

exe_opt_df['target_price'] = (exe_opt_df['average_price'] * 1.10).astype(int)
exe_opt_df['tPL%'] = ((exe_opt_df['target_price'] - exe_opt_df['average_price']) / exe_opt_df['average_price']) * 100

lmt_ord_df = exe_opt_df[exe_opt_df['quantity'] > 0]
lmt_ord_df = lmt_ord_df[['tradingsymbol', 'quantity', 'average_price', 'PL%', 'target_price', 'tPL%']]

open_orders = place_sell_limit_orders(lmt_ord_df, broker)

print("━" * 42)

import numpy as np
import calendar
from datetime import datetime

# Get the current and next month abbreviations
now = datetime.now()
current_month_abbr = now.strftime('%b').upper()  # e.g., 'AUG'
next_month = (now.month % 12) + 1  # Get next month number (1-12)
next_month_abbr = calendar.month_abbr[next_month].upper()  # e.g., 'SEP'

# Assuming `opt_df` is already defined earlier in the code
print_df = exe_opt_df.copy()
print_df = print_df[print_df['PL%'] > 0]
print_df['CP'] = print_df['key'].apply(lambda x: '🟠' if x.endswith('PE') else ('🟢' if x.endswith('CE') else None))
print_df['group'] = print_df['key'].str.extract(r'^(B|N)', expand=False)
print_df['key'] = print_df['key'].str.replace('BANKNIFTY24', 'B').str.replace('NIFTY24', 'N')
print_df['strike'] = print_df['key'].str.replace(r'(PE|CE)$', '', regex=True)
print_df['PL%'] = print_df['PL%'].round(2)
print_df['tgtoptsmadepth'] = print_df['tgtoptsmadepth'].round(2)
# Set 'MN' based on the month abbreviation in 'key'
print_df['MN'] = np.where(
    print_df['key'].str.contains(current_month_abbr),
    '⌛',
    np.where(print_df['key'].str.contains(next_month_abbr), '🔢', None)
)
print_df = print_df[['MN', 'strike', 'Invested', 'qty', 'PL%', 'm2m', 'PnL', 'CP', 'group','tgtoptsmadepth']]
filtered_data = print_df.query('qty > 0')[['MN', 'strike', 'qty','tgtoptsmadepth', 'CP', 'PL%', 'PnL']]
filtered_data['PL%'] = filtered_data['PL%'].astype(int)
print("━" * 42)
if filtered_data.empty:
    print(f"{GREY}Still fishing🔎🎣, nothing surfaced yet.🐟{RESET}")
else:
    print(f"Surfaced .🐟, let's try to catch them 🔎🎣{RESET}")
    print(filtered_data.to_string(header=False, index=False, col_space=[2, 10, 3, 4, 2, 4, 7]))

