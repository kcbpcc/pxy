import sys
import traceback
import pandas as pd
import requests
import logging
from datetime import datetime, timedelta
import calendar
from login_get_kite import get_kite, remove_token
from cnstpxy import dir_path
from cmbddfpxy import process_data
from smapxy import check_index_status
from utcpxy import peak_time
from depthpxy import calculate_consecutive_candles
from mktpxy import get_market_check
from predictpxy import predict_market_sentiment
from bpredictpxy import predict_bnk_sentiment
from expdaypxy import get_last_weekday_of_current_month
from clorpxy import SILVER, UNDERLINE, RED, GREEN, YELLOW, RESET, BRIGHT_YELLOW, BRIGHT_RED, BRIGHT_GREEN, BOLD, GREY
import argparse
parser = argparse.ArgumentParser(description="Process some commands.")
parser.add_argument('command', nargs='?', choices=['l', 's'], default='s',
                    help="Command to run the program with. Defaults to 's' if not provided.")
args = parser.parse_args()

# Define function to get last weekday dates
last_wednesday_str = get_last_weekday_of_current_month(calendar.WEDNESDAY)
last_thursday_str = get_last_weekday_of_current_month(calendar.THURSDAY)

# Define the current year
current_year = datetime.now().year

# Convert string dates to datetime objects with current year
def parse_date(date_str):
    return datetime.strptime(f"{date_str}-{current_year}", '%d-%b-%Y')

last_wednesday = parse_date(last_wednesday_str)
last_thursday = parse_date(last_thursday_str)

def business_days_diff(start_date, end_date):
    """Calculate business days between two dates."""
    if start_date > end_date:
        start_date, end_date = end_date, start_date
    return len(pd.bdate_range(start_date, end_date))

def send_telegram_message(message):
    bot_token = '7141714085:AAHlyEzszCy9N-L6wO1zSAkRwGdl0VTQCFI'
    user_usernames = ('-4282665161',)
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
        print(f"Placing order for {tradingsymbol} with quantity {quantity}")
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

def exit_options(blnc_opt_df, broker):
    try:
        if 'Target' not in blnc_opt_df.columns:
            print("Target column is missing in the DataFrame.")
            return

        for index, row in blnc_opt_df.iterrows():
            total_pl_percentage = row['PL%']
            tgtoptsmadepth = row['Target']
            
            #print(f"Checking conditions for {row['key']}: PL% = {total_pl_percentage}, Target = {tgtoptsmadepth}")
            if total_pl_percentage > tgtoptsmadepth:
                #print(f"Conditions met for {row['key']}, placing order")
                place_order(row['key'], row['qty'], 'SELL', 'MARKET', 'NRML', broker)
                message = (
                    f"🛬🛬🛬 😧😧😧 EXIT order placed {row['key']} successfully.\n"
                    f"🎯 Target PL%: {round(tgtoptsmadepth, 4)}%\n"
                    f"🏆 Reached PL%: {round(total_pl_percentage, 2)}%\n"
                    f"💰 Booked Profit: {row['PnL']}\n"
                )
                print(message)
                send_telegram_message(message)
            else:
                pass
                #print(f"Conditions not met for {row['key']}, skipping order")
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
blnc_opt_df = combined_df[combined_df['key'].str.contains('NFO:', case=False)].copy()
blnc_opt_df['key'] = blnc_opt_df['key'].str.replace('NFO:', '') 
blnc_opt_df['PL%'] = (blnc_opt_df['PnL'] / blnc_opt_df['Invested']) * 100
blnc_opt_df['PL%'] = blnc_opt_df['PL%'].fillna(0)

blnc_opt_df['strike'] = blnc_opt_df['key'].str.replace(r'(PE|CE)$', '', regex=True)

# Get the current month's abbreviation
current_month_abbr = datetime.now().strftime('%b').upper()  # e.g., 'JAN', 'FEB', 'MAR'

# Select only the key, qty, tradingsymbol, Invested, value, and PL% columns and filter by current month's abbreviation
selected_df = blnc_opt_df[['key', 'qty', 'Invested', 'value', 'PL%', 'PnL']]
selected_df.columns = ['key', 'qty', 'Invested', 'value', 'PL%', 'PnL']  # Rename columns for clarity
filtered_df = selected_df[selected_df['key'].str.contains(current_month_abbr)].copy()

# Add date column based on trading symbol
def add_date(row):
    if row['key'].startswith('BANKNIFTY'):
        return last_wednesday  # Return full date
    elif row['key'].startswith('NIFTY'):
        return last_thursday  # Return full date
    else:
        return None

filtered_df.loc[:, 'Date'] = filtered_df.apply(add_date, axis=1)

# Add 'Today' column with the current date
filtered_df.loc[:, 'Today'] = datetime.now()

# Add 'Diff' column showing the difference in working days between 'Date' and 'Today'
filtered_df.loc[:, 'Diff'] = filtered_df.apply(lambda row: business_days_diff(row['Date'], row['Today']), axis=1)

# Extract day for 'Date' and 'Today'
filtered_df.loc[:, 'Date'] = filtered_df['Date'].dt.day
filtered_df.loc[:, 'Today'] = filtered_df['Today'].dt.day

# Add 'Target' column with the specified condition
def calculate_target(x):
    print(f"x: {x}")  # Print the value of x
    if x == 0:
        return 99
    elif x < 10:
        return (100 - (x * 9)) * -1
    else:
        return 105

filtered_df.loc[:, 'Target'] = filtered_df['Diff'].apply(calculate_target)


# Reorder columns as requested
final_df = filtered_df[filtered_df['qty'] > 0][['key', 'qty', 'Invested', 'value', 'PL%', 'PnL', 'Date', 'Today', 'Diff', 'Target']]
row_count = final_df.shape[0]
sum_invested = final_df['Invested'].sum()
print("━" * 42)
print(f"🤔..🤔..Recovering {YELLOW}{str(row_count).zfill(2)}{RESET} opts worth {YELLOW}{str(sum_invested).zfill(7)}{RESET}🤔")
filtered_df['PL%'] = filtered_df['PL%'].astype(int)
final_prnt_df = filtered_df[['key', 'qty', 'PL%', 'Target', 'PnL']].copy()

if args.command == 'l':
    final_prnt_str = final_prnt_df.to_string(index=False, header=False)
    right_aligned_output = '\n'.join([line.rjust(42) for line in final_prnt_str.split('\n')])
    print(right_aligned_output)


# Call the function to exit options
exit_options(final_df, broker)
