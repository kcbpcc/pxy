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
from vixpxy import get_vixpxy
from clorpxy import SILVER, UNDERLINE, RED, GREEN, YELLOW, RESET, BRIGHT_YELLOW, BRIGHT_RED, BRIGHT_GREEN, BOLD, GREY
# Check index status
bsma = check_index_status('^NSEBANK')
nsma = check_index_status('^NSEI')
nvix, bvix = get_vixpxy()

# Get peak time
peak = peak_time()

# Telegram bot token and user IDs
bot_token = '7141714085:AAHlyEzszCy9N-L6wO1zSAkRwGdl0VTQCFI'
user_usernames = ('-4282665161',)

def calculate_totals(combined_df):
    if not combined_df.empty:
        extras_df = combined_df[(combined_df['exchange'] == 'NFO') & (combined_df['sell_quantity'] > 0)].copy()
        #total_opt_pnl = int(extras_df['unrealised'].sum())
        total_opt_pnl = int(extras_df['unrealised'].sum()) + ((-1) * int(extras_df['PnL'].sum()))
        #print(total_opt_pnl)
    else:
        total_opt_pnl = 0
    return total_opt_pnl

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

def exit_options(exe_opt_df, broker):
    total_opt_pnl = calculate_totals(exe_opt_df)
    try:
        for index, row in exe_opt_df.iterrows():
            total_pl_percentage = row['PL%']
            tgtoptsmadepth = row['tgtoptsmadepth']
            
            if total_pl_percentage > tgtoptsmadepth and row['PnL'] > 400:
                place_order(row['key'], row['qty'], 'SELL', 'MARKET', 'NRML', broker)
                message = (
                    f"🛬🛬🛬 🎯🎯🎯 EXIT order placed {row['key']} successfully.\n"
                    f"🎯 Target PL%: {tgtoptsmadepth}%\n"
                    f"🏆 Reached PL%: {round(total_pl_percentage, 2)}%\n"
                    f"📉 Sell Price: {row['ltp']}\n"
                    f"📈 Buy Price: {row['avg']}\n"
                    f"💰 Booked Profit: {row['PnL']}\n"
                    f"Total Booked:💰 {total_opt_pnl} 📣"
                )
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

# Process data and prepare exe_opt_df
combined_df = process_data()
exe_opt_df = combined_df[combined_df['key'].str.contains('NFO:', case=False)].copy()
exe_opt_df['key'] = exe_opt_df['key'].str.replace('NFO:', '') 
exe_opt_df['PL%'] = (exe_opt_df['PnL'] / exe_opt_df['Invested']) * 100
exe_opt_df['PL%'] = exe_opt_df['PL%'].fillna(0)

# Define the 'strike' column
exe_opt_df['strike'] = exe_opt_df['key'].str.replace(r'(PE|CE)$', '', regex=True)

# Calculate tgtoptsma for each row using global variable bsma
def compute_tgtoptsma(row):
    global bsma
    global nsma
    
    key = row['key']
    
    if (bsma == "up" and key.startswith("BANK") and "CE" in key) or (bsma == "down" and key.startswith("BANK") and "PE" in key):
        return 4
    elif (nsma == "up" and key.startswith("NIFTY") and "CE" in key) or (nsma == "down" and key.startswith("NIFTY") and "PE" in key):
        return 4
    else:
        return 4

exe_opt_df['tgtoptsma'] = exe_opt_df.apply(compute_tgtoptsma, axis=1)

# Calculating depths for NSEBANK and NSEI indices
bcedepth, bpedepth = calculate_consecutive_candles("^NSEBANK")
ncedepth, npedepth = calculate_consecutive_candles("^NSEI")

def compute_depth(row):
    try:
        # Ensure the following variables are defined and have appropriate values before this function call
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
        # Optionally log the exception e if needed
        return 5


exe_opt_df['tgtoptsmadepth'] = exe_opt_df.apply(compute_depth, axis=1)
# Dump exe_opt_df to CSV file
#csv_filename = 'cntrloptpxy.csv'  # You can modify this filename as needed
#exe_opt_df.to_csv(csv_filename, index=False)
#print(f"Data successfully dumped to {csv_filename}")
if peak != 'PEAKSTART':
    exit_options(exe_opt_df, broker)

# Import required color formatting constants
from colorpxy import BRIGHT_RED, BRIGHT_GREEN, RESET



# Define left and right alignment format strings
left_aligned_format = "{:<42}"
right_aligned_format = "{:>42}"

# Prepare output lines
output_lines = []

output_lines.append(
    left_aligned_format.format(f"BPE-TGT:{BRIGHT_RED if bpedepth < 6 else BRIGHT_GREEN}{bpedepth}{RESET}") +
    right_aligned_format.format(f"NCE-TGT:{BRIGHT_GREEN if ncedepth < 6 else BRIGHT_RED}{ncedepth}{RESET}")
)
output_lines.append(
    left_aligned_format.format(f"BCE-TGT:{BRIGHT_RED if bcedepth < 6 else BRIGHT_GREEN}{bcedepth}{RESET}") +
    right_aligned_format.format(f"NCE-TGT:{BRIGHT_GREEN if ncedepth < 6 else BRIGHT_RED}{ncedepth}{RESET}")
)

# Join and print the formatted output
full_output = '\n'.join(output_lines)
print(full_output)

