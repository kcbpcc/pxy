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
mktpredict = predict_market_sentiment()
bmktpredict = predict_bnk_sentiment()
bonemincandlesequance, bmktpxy = get_market_check('^NSEBANK')
nonemincandlesequance, nmktpxy = get_market_check('^NSEI')
from clorpxy import SILVER, UNDERLINE, RED, GREEN, YELLOW, RESET, BRIGHT_YELLOW, BRIGHT_RED, BRIGHT_GREEN, BOLD, GREY

bsma = check_index_status('^NSEBANK')
nsma = check_index_status('^NSEI')
arrow_map = {"Buy": "⤴", "Sell": "⤵", "Bull": "↗", "Bear": "↘"}
peak = peak_time()

column_width = 30
left_aligned_format = "{:<" + str(column_width) + "}"
right_aligned_format = "{:>" + str(column_width) + "}"
output_lines = []
output_lines.append(left_aligned_format.format(f"BANKNIFTY ━━ {BRIGHT_GREEN if bmktpredict == 'RISE' else BRIGHT_RED if bmktpredict == 'FALL' else BRIGHT_YELLOW}{bmktpredict} {arrow_map.get(bmktpxy, '')}{RESET}") +
                    right_aligned_format.format(f"{BRIGHT_GREEN if mktpredict == 'RISE' else BRIGHT_RED if mktpredict == 'FALL' else BRIGHT_YELLOW} {mktpredict} {arrow_map.get(nmktpxy, '')}{RESET} ━━ NIFTYNDEX")) 
full_output = '\n'.join(output_lines)
print(full_output)
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
                    f"🎯 Target PL%: {round(tgtoptsmadepth, 4)}%\n"
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
    exit_options(exe_opt_df, broker)

#############################################################################################################################################################################################################################
widths = {'tradingsymbol': '22', 'qty': '3', 'PL%': '5','tgtoptsmadepth': '5','PnL': '7'}

def format_row(row):
    symbol = row['tradingsymbol'][:int(widths['tradingsymbol'])].ljust(int(widths['tradingsymbol']))
    qty = f"{int(row['qty'])}".rjust(int(widths['qty']))
    pl_pct = f"{row['PL%']:.1f}".rjust(int(widths['PL%']))
    tgtoptsmadepth = f"{row['tgtoptsmadepth']:.1f}".rjust(int(widths['tgtoptsmadepth']))
    pnl = f"{int(row['PnL'])}".rjust(int(widths['PnL']))
    return f"{symbol}{qty}{pl_pct}{tgtoptsmadepth}{pnl}"

filtered_df = exe_opt_df.query('qty > 0 and `PL%` > 0')

if filtered_df.empty:
    print("Still fishing🔎🎣, nothing surfaced yet.🕵")
else:
    formatted_rows = [format_row(row) for _, row in filtered_df.iterrows()]
    print("━" * 42)
    print('\n'.join(formatted_rows))
    print("━" * 42)

#############################################################################################################################################################################################################################
data = {
    'key': ['BANKCE', 'BANKPE', 'NIFTYCE', 'NIFTYPE'],
    'tgtoptsma': [4, 4, 4, 4]  # Hardcoded tgtoptsma values
}

vdf = pd.DataFrame(data)

vdf['computed_depth'] = vdf.apply(compute_depth, axis=1)

vdf['BCE-DPT'] = vdf.apply(lambda row: row['computed_depth'] if row['key'] == 'BANKCE' else None, axis=1)
vdf['BPE-DPT'] = vdf.apply(lambda row: row['computed_depth'] if row['key'] == 'BANKPE' else None, axis=1)
vdf['NCE-DPT'] = vdf.apply(lambda row: row['computed_depth'] if row['key'] == 'NIFTYCE' else None, axis=1)
vdf['NPE-DPT'] = vdf.apply(lambda row: row['computed_depth'] if row['key'] == 'NIFTYPE' else None, axis=1)

expected_columns = ['BCE-DPT', 'BPE-DPT', 'NCE-DPT', 'NPE-DPT']
missing_columns = [col for col in expected_columns if col not in vdf.columns]
if missing_columns:
    raise ValueError(f"Missing columns in DataFrame: {missing_columns}")

column_width = 30

left_aligned_format = f"{{:<{column_width}}}"
right_aligned_format = f"{{:>{column_width}}}"

bce_dpt_value = round(vdf['BCE-DPT'].dropna().values[0], 2) if not vdf['BCE-DPT'].isna().all() else 'None'
bpe_dpt_value = round(vdf['BPE-DPT'].dropna().values[0], 2) if not vdf['BPE-DPT'].isna().all() else 'None'
nce_dpt_value = round(vdf['NCE-DPT'].dropna().values[0], 2) if not vdf['NCE-DPT'].isna().all() else 'None'
npe_dpt_value = round(vdf['NPE-DPT'].dropna().values[0], 2) if not vdf['NPE-DPT'].isna().all() else 'None'

output_lines = []

output_lines.append(
    left_aligned_format.format(
        f"NPE-DPT:{BRIGHT_GREEN if npe_dpt_value != 'None' and npe_dpt_value > 6 else GREY}{npe_dpt_value}{RESET}"
    ) +
    right_aligned_format.format(
        f"NCE-DPT:{BRIGHT_GREEN if nce_dpt_value != 'None' and nce_dpt_value > 6 else GREY}{nce_dpt_value}{RESET}"
    )
)

output_lines.append(
    left_aligned_format.format(
        f"BPE-DPT:{GREY if bpe_dpt_value != 'None' and bpe_dpt_value < 6 else BRIGHT_GREEN}{bpe_dpt_value}{RESET}"
    ) +
    right_aligned_format.format(
        f"BCE-DPT:{GREY if bce_dpt_value != 'None' and bce_dpt_value < 6 else BRIGHT_GREEN}{bce_dpt_value}{RESET}"
    )
)

full_output = '\n'.join(output_lines)
print(full_output)
print("━" * 42)
