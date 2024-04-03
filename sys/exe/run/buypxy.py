# PXYImports (place at the beginning)
from toolkit.logger import Logger
from toolkit.currency import round_to_paise
from toolkit.utilities import Utilities
from login_get_kite import get_kite, remove_token
from cnstpxy import dir_path, fileutils, buybuff, max_target
from trndlnpxy import Trendlyne
import pandas as pd
import traceback
import sys
import os
from fundpxy import calculate_decision
import asyncio
import logging
import telegram

# Configure logging
logging.basicConfig(level=logging.INFO)
logging = Logger(30, dir_path + "main.log")

# Set up black file path
black_file = dir_path + "blacklist.txt"

# Save the original sys.stdout
original_stdout = sys.stdout

# Define lst_tlyne before the try-except block
lst_tlyne = []

try:
    # Redirect sys.stdout to 'output.txt'
    with open('output.txt', 'w') as file:
        sys.stdout = file

        try:
            broker = get_kite(api="bypass", sec_dir=dir_path)
        except Exception as e:
            remove_token(dir_path)
            print(traceback.format_exc())
            logging.error(f"{str(e)} unable to get holdings")
            sys.exit(1)

finally:
    # Reset sys.stdout to its original value
    sys.stdout = original_stdout

# Call the calculate_decision function to get the decision
decision = calculate_decision()

if decision == "YES":
    try:
        # Read the fileHPdf.csv directly
        df_fileHPdf = pd.read_csv('empty.csv', encoding='latin1')
    
        if df_fileHPdf.empty:
            print("The file is empty. No data to process.")
        elif 'tradingsymbol' not in df_fileHPdf.columns:
            print("No 'tradingsymbol' column found in the file.")
        else:
            # Extract tradingsymbols from df_fileHPdf
            lst = df_fileHPdf['tradingsymbol'].tolist()
    
            # get list from Trendlyne
            lst_dct_tlyne = Trendlyne().entry()
            if lst_dct_tlyne and any(lst_dct_tlyne):
                lst_tlyne = [dct['tradingsymbol'] for dct in lst_dct_tlyne]
    
    except pd.errors.EmptyDataError:
        # Handle the case when the file is empty
        print("The file is empty. No data to process.")
    
    except Exception as e:
        # Handle other exceptions
        print(f"An error occurred: {e}")

    # Check if lst_tlyne is not empty before using it
    if lst_tlyne:
        try:
            if any(lst_tlyne):
                logging.info(f"reading trendlyne ...{lst_tlyne}")
                lst_tlyne = [x for x in lst_tlyne if x not in lst]
                logging.info(f"filtered from holdings and positions: {lst}")

                # get lists from orders
                lst_dct_orders = broker.orders

                if lst_dct_orders and any(lst_dct_orders):
                    symbols_orders = [dct['symbol'] for dct in lst_dct_orders]
                else:
                    symbols_orders = []

                # Combine symbols orders
                all_symbols = symbols_orders

                # Assuming lst_tlyne is defined somewhere before this block
                lst_tlyne = lst_tlyne if lst_tlyne else []  # Initialize lst_tlyne if not defined

                # Filter lst_tlyne based on combined symbols
                lst_tlyne = [x for x in lst_tlyne if x not in all_symbols]

                logging.info(f"filtered from orders, these are not in orders ...{lst_tlyne}")

        except Exception as e:
            print(traceback.format_exc())
            logging.error(f"{str(e)} unable to read positions")
            sys.exit(1)
    else:
        print("lst_tlyne is not defined or is empty.")
        

elif decision == "NO":
    # Perform actions for "NO"
    print("\033[91mNo sufficient funds available \033[0m")
    print("-" * 42)
