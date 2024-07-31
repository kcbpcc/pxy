from cntrlcoptpxy import *

# Initialization
broker = initialize_broker()

# Nifty-specific
nifty_vix, _ = get_vixpxy()
n_vix = nifty_vix / 2
nsma = check_index_status('^NSEI')
ncedepth, npedepth = calculate_consecutive_candles('^NSEI')

# Nifty-specific depth calculation
def compute_depth(row):
    try:
        if "CE" in row['key'] and ncedepth > 1:
            return max(row['tgtoptsma'], (n_vix + 9 - ncedepth))
        elif "PE" in row['key'] and npedepth > 1:
            return max(row['tgtoptsma'], (n_vix + 9 - npedepth))
        else:
            return 5
    except Exception as e:
        return 5

combined_df = process_data()
exe_opt_df = combined_df[combined_df['key'].str.contains('NFO:', case=False)].copy()
exe_opt_df = prepare_data_and_apply_depth('^NSEI', exe_opt_df, nsma, n_vix)
exe_opt_df['tgtoptsmadepth'] = exe_opt_df.apply(compute_depth, axis=1)

if peak_time() != 'PEAKSTART':
    exit_options(exe_opt_df, broker)

# Output Formatting
widths = {'tradingsymbol': '22', 'qty': '3', 'PL%': '5', 'tgtoptsmadepth': '5', 'PnL': '7'}
filtered_df = exe_opt_df.query('qty > 0 and `PL%` > 0')

if filtered_df.empty:
    print("Still fishing🔎🎣, nothing surfaced yet.🕵")
else:
    formatted_rows = [format_row(row, widths) for _, row in filtered_df.iterrows()]
    print("━" * 42)
    print('\n'.join(formatted_rows))

