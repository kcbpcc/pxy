from common import *
from vixpxy import get_vixpxy

# Initialization
bot_token = 'YOUR_BOT_TOKEN'
user_usernames = ('YOUR_USER_ID',)
try:
    sys.stdout = open('nifty_output.txt', 'w')
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

# Specific to Nifty
mktpredict = predict_market_sentiment()
nmktpxy = get_market_check('^NSEI')
nsma = check_index_status('^NSEI')
n_vix, _ = get_vixpxy()
nvix = n_vix / 2

combined_df = process_data()
exe_opt_df = combined_df[combined_df['key'].str.contains('NFO:', case=False)].copy()
exe_opt_df['key'] = exe_opt_df['key'].str.replace('NFO:', '') 
exe_opt_df['PL%'] = (exe_opt_df['PnL'] / exe_opt_df['Invested']) * 100
exe_opt_df['PL%'] = exe_opt_df['PL%'].fillna(0)

exe_opt_df['strike'] = exe_opt_df['key'].str.replace(r'(PE|CE)$', '', regex=True)

def compute_tgtoptsma(row):
    if (nsma == "up" and "CE" in row['key']) or (nsma == "down" and "PE" in row['key']):
        return 7
    else:
        return 5

exe_opt_df['tgtoptsma'] = exe_opt_df.apply(compute_tgtoptsma, axis=1)

ncedepth, npedepth = calculate_consecutive_candles("^NSEI")

def compute_depth(row):
    try:
        global ncedepth, npedepth, nvix
        if "CE" in row['key'] and ncedepth > 1:
            return max(row['tgtoptsma'], (nvix + 9 - ncedepth))
        elif "PE" in row['key'] and npedepth > 1:
            return max(row['tgtoptsma'], (nvix + 9 - npedepth))
        else:
            return 5
    except Exception as e:
        return 5

exe_opt_df['tgtoptsmadepth'] = exe_opt_df.apply(compute_depth, axis=1)

if peak != 'PEAKSTART':
    exit_options(exe_opt_df, broker, bot_token, user_usernames)

# Output Formatting
widths = {'tradingsymbol': '22', 'qty': '3', 'PL%': '5', 'tgtoptsmadepth': '5', 'PnL': '7'}

filtered_df = exe_opt_df.query('qty > 0 and `PL%` > 0')

if filtered_df.empty:
    print("Still fishing🔎🎣, nothing surfaced yet.🕵")
else:
    formatted_rows = [format_row(row, widths) for _, row in filtered_df.iterrows()]
    print("━" * 42)
    print('\n'.join(formatted_rows))
