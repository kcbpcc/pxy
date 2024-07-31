from cntrlcoptpxy import *

# Initialization
broker = initialize_broker()

# Bank Nifty-specific
_, bank_nifty_vix = get_vixpxy()
b_vix = bank_nifty_vix / 2
bsma = check_index_status('^NSEBANK')
bcedepth, bpedepth = calculate_consecutive_candles('^NSEBANK')

# Bank Nifty-specific depth calculation
def compute_depth(row):
    try:
        if "CE" in row['key'] and bcedepth > 1:
            return max(row['tgtoptsma'], (b_vix + 9 - bcedepth))
        elif "PE" in row['key'] and bpedepth > 1:
            return max(row['tgtoptsma'], (b_vix + 9 - bpedepth))
        else:
            return 5
    except Exception as e:
        return 5

combined_df = process_data()
exe_opt_df = combined_df[combined_df['key'].str.contains('NFO:', case=False)].copy()
exe_opt_df = prepare_data_and_apply_depth('^NSEBANK', exe_opt_df, bsma, b_vix)
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

