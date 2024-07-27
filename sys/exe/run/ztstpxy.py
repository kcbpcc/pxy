import sys
import traceback
import pandas as pd
import requests
import logging
from datetime import datetime
import numpy as np
import calendar
from expdaypxy import get_last_weekday_of_current_month
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

# Define current year and last weekday dates
current_year = datetime.now().year
last_wednesday = get_last_weekday_of_current_month(calendar.WEDNESDAY)
last_thursday = get_last_weekday_of_current_month(calendar.THURSDAY)

# Helper functions
def add_date(row):
    """ Returns a single date object based on the trading symbol. """
    if row['tradingsymbol'].startswith('BANKNIFTY'):
        return last_wednesday
    elif row['tradingsymbol'].startswith('NIFTY'):
        return last_thursday
    else:
        return None

def calculate_working_days(date_obj):
    """ Calculates the number of business days between date_obj and today. """
    if pd.isna(date_obj) or date_obj is None:
        return None
    try:
        today = datetime.now().date()
        return np.busday_count(date_obj, today)
    except Exception as e:
        print(f"Error calculating working days: {e}")
        return None

# Main script execution
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
blnc_opt_df = combined_df[combined_df['key'].str.contains('NFO:', case=False)].copy()
blnc_opt_df['key'] = blnc_opt_df['key'].str.replace('NFO:', '')
blnc_opt_df['PL%'] = (blnc_opt_df['PnL'] / blnc_opt_df['Invested']) * 100
blnc_opt_df['PL%'] = blnc_opt_df['PL%'].fillna(0)

# Extract strike prices
blnc_opt_df['strike'] = blnc_opt_df['key'].str.replace(r'(PE|CE)$', '', regex=True)

# Filter by months
filtered_df = blnc_opt_df[
    blnc_opt_df['tradingsymbol'].str.contains('JAN|FEB|MAR', case=False)
].copy()

# Add the 'Date' column as the day of the month
filtered_df['Date'] = filtered_df.apply(lambda row: add_date(row).day if add_date(row) else None, axis=1)

# Calculate difference in working days between current date and Date
def calculate_days_difference(day):
    """ Calculates days difference between today and a given day of the month. """
    if day is None:
        return None
    try:
        today = datetime.now().date()
        target_date = today.replace(day=day)
        return calculate_working_days(target_date)
    except Exception as e:
        print(f"Error calculating days difference: {e}")
        return None

filtered_df['Days_Difference'] = filtered_df['Date'].apply(calculate_days_difference)

# Reorder columns as requested
final_df = filtered_df[['tradingsymbol', 'Invested', 'value', 'PL%', 'Date', 'Days_Difference']]

print(final_df.to_string(index=False))




