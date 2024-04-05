import sys
import traceback
import pandas as pd
from login_get_kite import get_kite, remove_token
from cnstpxy import dir_path
from toolkit.logger import Logger
import csv
import os
import sys
import traceback
import logging

file_path = 'filePnL.csv'
logging = Logger(30, dir_path + "main.log")

try:
    sys.stdout = open('output.txt', 'w')
    broker = get_kite(api="bypass", sec_dir=dir_path)
except Exception as e:
    remove_token(dir_path)
    print(traceback.format_exc())
    logging.error(f"{str(e)} unable to get holdings")
    sys.exit(1)
finally:
    # Ensure to close the file and restore stdout
    if sys.stdout != sys.__stdout__:
        sys.stdout.close()
        sys.stdout = sys.__stdout__

from cmbddfpxy import process_data
combined_df = process_data()
opt_df = combined_df[combined_df['key_column_name'].str.contains('NFO', case=False)].copy()
opt_df['CP'] = opt_df['key'].apply(lambda x: '🟥' if x.endswith('PE') else ('🟩' if x.endswith('CE') else None))
opt_df.loc[:, 'key'] = opt_df['key'].str.replace('NFO:', '')  # Remove 'NFO:' from the 'key' column
opt_df = opt_df[['key', 'Invested', 'qty', 'PnL', 'CP']]

# Print the DataFrame with values aligned to the right and width of 42 spaces
print(opt_df.to_string(index=False, header=False, justify='right', col_space=42))

