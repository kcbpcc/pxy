from common import *

# Initialization
broker = initialize_broker()

# Specific to Bank Nifty
bmktpredict = predict_bnk_sentiment()
bmktpxy = get_market_check('^NSEBANK')
bsma = check_index_status('^NSEBANK')
_, b_vix = get_vixpxy()
bvix = b_vix / 2

combined_df = process_data()
exe_opt_df = combined_df[combined_df['key'].str.contains('NFO:', case=False)].copy()
exe_opt_df = prepare_data_and_apply_depth('^NSEBANK', exe_opt_df, bsma, bvix)

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
