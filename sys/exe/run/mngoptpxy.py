import sys
import traceback
import pandas as pd
import requests
import logging
from datetime import datetime
import calendar
from login_get_kite import get_kite, remove_token
from cnstpxy import dir_path
from cmbddfpxy import process_data
from expdaypxy import get_last_weekday_of_current_month
from clorpxy import SILVER, UNDERLINE, RED, GREEN, YELLOW, RESET, BRIGHT_YELLOW, BRIGHT_RED, BRIGHT_GREEN, BOLD, GREY
from mktpxy import get_market_check
import argparse

# Argument parsing
parser = argparse.ArgumentParser(description="Process some commands.")
parser.add_argument('command', nargs='?', choices=['l', 's'], default='s',
                    help="Command to run the program with. Defaults to 's' if not provided.")
args = parser.parse_args()

# Define function to get last weekday dates
last_wednesday_str = get_last_weekday_of_current_month(calendar.WEDNESDAY)
last_thursday_str = get_last_weekday_of_current_month(calendar.THURSDAY)

# Define the current year
current_year = datetime.now().year
now = datetime.now()
current_month_abbr = now.strftime('%b')

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
    user_usernames = ['-4282665161']
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
            
            if total_pl_percentage > tgtoptsmadepth:
                place_order(row['key'], row['qty'], 'SELL', 'MARKET', 'NRML', broker)
                message = (
                    f"🛬🛬🛬 😧😧😧 EXIT order placed {row['key']} successfully.\n"
                    f"🎯 Target PL%: {round(tgtoptsmadepth, 4)}%\n"
                    f"🏆 Reached PL%: {round(total_pl_percentage, 2)}%\n"
                    f"💰 Booked Profit: {row['PnL']}\n"
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
blnc_opt_df = combined_df[
    (combined_df['key'].str.contains('NFO:', case=False, na=False)) &
    (combined_df['qty'] > 0) &
    (combined_df['key'].notna())
].copy()

blnc_opt_df['key'] = blnc_opt_df['key'].str.replace('NFO:', '', regex=False) 
blnc_opt_df['PL%'] = (blnc_opt_df['PnL'] / blnc_opt_df['Invested']) * 100
blnc_opt_df['PL%'] = blnc_opt_df['PL%'].fillna(0)

blnc_opt_df['strike'] = blnc_opt_df['key'].str.replace(r'(PE|CE)$', '', regex=True)

# Get the current month's abbreviation
current_month_abbr = datetime.now().strftime('%b').upper()

blnc_opt_df = blnc_opt_df[['key', 'qty', 'Invested', 'value', 'PL%', 'PnL']]
blnc_opt_df = blnc_opt_df[blnc_opt_df['qty'] > 0]
blnc_opt_df = blnc_opt_df[blnc_opt_df['key'].str.contains(current_month_abbr)].copy()
blnc_opt_df = blnc_opt_df.dropna(how='all')

def add_date(row):
    if row['key'].startswith('BANKNIFTY'):
        return last_wednesday
    elif row['key'].startswith('NIFTY'):
        return last_thursday
    else:
        return None

blnc_opt_df.loc[:, 'Date'] = blnc_opt_df.apply(add_date, axis=1)
blnc_opt_df.loc[:, 'Today'] = datetime.now()
blnc_opt_df.loc[:, 'Diff'] = blnc_opt_df.apply(lambda row: business_days_diff(row['Date'], row['Today']), axis=1)

blnc_opt_df['Date'] = blnc_opt_df['Date'].dt.day
blnc_opt_df['Today'] = blnc_opt_df['Today'].dt.day

blnc_opt_df['Target'] = blnc_opt_df['Diff'].apply(lambda x: (100 - (x * 9)) * -1 if x < 10 else 107)
blnc_opt_df = blnc_opt_df[blnc_opt_df['qty'] > 0]

final_df = blnc_opt_df[blnc_opt_df['Target'] < 0][['key', 'qty', 'Invested', 'value', 'PL%', 'PnL', 'Date', 'Today', 'Diff', 'Target']]
row_count = final_df.shape[0]
sum_invested = final_df['Invested'].sum()

print(f"{GREY}🤔..🤔..Recovering {str(row_count).zfill(2)} opts worth {str(sum_invested).zfill(7)}🤔{RESET}")
width = 42
line1 = f"B:{last_wednesday_str}"
line2 = f"N:{last_thursday_str}"

# Combine both lines and center them in a 42-character wide field
combined_lines = f"{line1} ⚖     {BRIGHT_YELLOW}{current_month_abbr}{RESET}  {str(sum_invested).zfill(7)}    ⚖  {line2}"
BRIGHT_YELLOW = '\033[93m'
RESET = '\033[0m'    # Reset to default color
print(f"{SILVER}{combined_lines:^{width}}{RESET}")


blnc_ex_prnt_df = (
    blnc_opt_df.query('Target < 0')
    .assign(PL_percent=blnc_opt_df['PL%'].astype(int))
    .rename(columns={'PL_percent': 'PL%'})
    .assign(key=lambda x: x['key'].str.replace('BANKNIFTY', 'B').str.replace('NIFTY', 'N'))
    .fillna({'qty': 0, 'PL%': 0, 'Target': 0, 'PnL': 0})
    .astype({'qty': 'int', 'PL%': 'int', 'Target': 'int', 'PnL': 'int'})
    [['key', 'qty', 'PL%', 'Target', 'PnL']]
)

if args.command == 'l':
    final_prnt_str = blnc_ex_prnt_df.to_string(index=False, header=False)
    right_aligned_output = '\n'.join([line.rjust(42) for line in final_prnt_str.split('\n')])
    print(right_aligned_output)
    print("━" * 42)

# Call the function to exit options
exit_options(final_df, broker)



###################################################################################"PXY® PreciseXceleratedYield Pvt Ltd™########################################################################################################################
###################################################################################"PXY® PreciseXceleratedYield Pvt Ltd™########################################################################################################################
###################################################################################"PXY® PreciseXceleratedYield Pvt Ltd™########################################################################################################################
###################################################################################"PXY® PreciseXceleratedYield Pvt Ltd™########################################################################################################################

final_avg_df = final_df[final_df['Target'] > 1]
avg_row_count = final_avg_df.shape[0]
avg_sum_invested = final_avg_df['Invested'].sum()
#print(f"{GREY}🤞..🤞...averaging {str(avg_row_count).zfill(2)} opts worth {str(avg_sum_invested).zfill(7)}🤞{RESET}")

blnc_avg_prnt_df = (
    blnc_opt_df.query('Target > 0')
    .assign(PL_percent=blnc_opt_df['PL%'].astype(int))
    .rename(columns={'PL_percent': 'PL%'})
    .assign(key=lambda x: x['key'].str.replace('BANKNIFTY', 'B').str.replace('NIFTY', 'N'))
    .fillna({'qty': 0, 'PL%': 0, 'Target': 0, 'PnL': 0})
    .astype({'qty': 'int', 'PL%': 'int', 'Target': 'int', 'PnL': 'int'})
    [['key', 'qty', 'PL%', 'Target', 'PnL']]
)

if args.command == 'l':
    final_prnt_str = blnc_avg_prnt_df.to_string(index=False, header=False)
    right_aligned_output = '\n'.join([line.rjust(42) for line in final_prnt_str.split('\n')])
    print(right_aligned_output)

# Import market check and action functions
bbnkonemincandlesequance, bmktpxy = get_market_check('^NSEBANK')
nonemincandlesequance, mktpxy = get_market_check('^NSEI')

from bftpxy import get_bnk_action
ha_bnk_action, bnk_power, bDay_Change, bOpen_Change = get_bnk_action()

from nftpxy import ha_nse_action, nse_power, Day_Change, Open_Change

# Additional logic to place buy orders for BANKNIFTY and NIFTY based on 'PL%' < -50
def place_buy_orders_based_on_pl(df, broker):
    try:
        for index, row in df.iterrows():
            if row['PL%'] < -50:
                qty = 0
                can_average = False

                if row['key'].startswith('BANKNIFTY'):
                    current_qty = row['qty']
                    if current_qty < 30 and current_qty + 15 <= 45:
                        qty = 15
                        if 'PE' in row['key']:
                            can_average = bnk_power > 0.85 and bmktpxy == 'Sell'
                        elif 'CE' in row['key']:
                            can_average = bnk_power < 0.15 and bmktpxy == 'Buy'
                elif row['key'].startswith('NIFTY'):
                    current_qty = row['qty']
                    if current_qty < 50 and current_qty + 25 <= 75:
                        qty = 25
                        if 'PE' in row['key']:
                            can_average = nse_power > 0.85 and mktpxy == 'Sell'
                        elif 'CE' in row['key']:
                            can_average = nse_power < 0.15 and mktpxy == 'Buy'
                else:
                    continue

                if can_average:
                    print(f"Placing BUY order for {row['key']} with quantity {qty}")
                    order_id = place_order(row['key'], qty, 'BUY', 'MARKET', 'NRML', broker)

                    if order_id:
                        message = (
                            f"🚀🚀🚀 🤑🤑🤑 BUY order placed {row['key']} successfully.\n"
                            f"PL%: {round(row['PL%'], 2)}%\n"
                            f"Quantity: {qty}\n"
                        )
                        print(message)
                        send_telegram_message(message)
                else:
                    pass
                    #print(f"Skipping BUY order for {row['key']} due to bnk_power, market conditions, or qty limit.")
    except Exception as e:
        print(f"Error placing BUY order: {e}")

# Call the function to place buy orders
place_buy_orders_based_on_pl(final_avg_df, broker)
