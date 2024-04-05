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
from clorpxy import SILVER, UNDERLINE, RED, GREEN, YELLOW, RESET, BRIGHT_YELLOW, BRIGHT_RED, BRIGHT_GREEN, BOLD, GREY

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
opt_df = combined_df[combined_df['key'].str.contains('NFO:', case=False)].copy()
opt_df['CP'] = opt_df['key'].apply(lambda x: '🟥' if x.endswith('PE') else ('🟩' if x.endswith('CE') else None))
opt_df.loc[:, 'key'] = opt_df['key'].str.replace('NFO:', '')  # Remove 'NFO:' from the 'key' column
opt_df = opt_df[['key', 'Invested', 'qty', 'PnL', 'CP']]

# Set the maximum width for display
pd.set_option('display.max_colwidth', 42)

# Convert DataFrame to string
formatted_lines = opt_df.to_string(index=False, header=False, justify='left', col_space=1, line_width=42).split('\n')

# Print each line with proper alignment and color
max_width = 42
for line in formatted_lines:
    color_code = (GREEN if (float(line.split()[-2]) > 0) else (RED if (float(line.split()[-2]) < 0) else (YELLOW if (float(line.split()[-2]) == 0) else RESET))) if (len(line.split()) >= 2 and line.split()[-2].replace('.', '').isdigit()) else RESET
    print(color_code + (line[:-3] + line[-3:].rjust(3)).rjust(41) + RESET)

