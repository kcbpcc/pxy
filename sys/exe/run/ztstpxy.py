import sys
import traceback
import pandas as pd
import requests
from datetime import datetime
import calendar
from login_get_kite import get_kite, remove_token
from cnstpxy import dir_path
from cmbddfpxy import process_data
from expdaypxy import get_last_weekday_of_current_month
import argparse
from clorpxy import SILVER, UNDERLINE, RED, GREEN, YELLOW, RESET, BRIGHT_YELLOW, BRIGHT_RED, BRIGHT_GREEN, BOLD, GREY
from nftpxy import ha_nse_action, nse_power, Day_Change, Open_Change  
from bftpxy import get_bnk_action
ha_bnk_action, bnk_power, bDay_Change, bOpen_Change = get_bnk_action()
from mktpxy import get_market_check
onemincandlesequance, mktpxy = get_market_check('^NSEI')
bnkonemincandlesequance, bmktpxy = get_market_check('^NSEBANK')

# Argument parsing
parser = argparse.ArgumentParser(description="Process some commands.")
parser.add_argument('--symbol', type=str, help="Symbol to filter for quantity check")
args = parser.parse_args()

# Date handling
last_wednesday_str = get_last_weekday_of_current_month(calendar.WEDNESDAY)
last_thursday_str = get_last_weekday_of_current_month(calendar.THURSDAY)

current_year = datetime.now().year

def parse_date(date_str):
    return datetime.strptime(f"{date_str}-{current_year}", '%d-%b-%Y')

last_wednesday = parse_date(last_wednesday_str)
last_thursday = parse_date(last_thursday_str)

def business_days_diff(start_date, end_date):
    """Calculate business days between two dates."""
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

def check_quantity_for_symbol(df, symbol):
    """Check quantities for a specific symbol and its corresponding options."""
    filtered_df = df[df['key'].str.contains(symbol, case=False, na=False)]
    if not filtered_df.empty:
        print(f"\nRows for symbol '{symbol}':")
        print(filtered_df[['key', 'qty', 'PL%']])

        filtered_df = filtered_df[['key', 'qty', 'PL%']].copy()

        # Check corresponding options
        if 'CE' in symbol:
            corresponding_symbol = symbol.replace('CE', 'PE')
        elif 'PE' in symbol:
            corresponding_symbol = symbol.replace('PE', 'CE')
        else:
            print("Symbol is neither CE nor PE.")
            return

        print(f"\nCorresponding symbol to check: {corresponding_symbol}")

        corresponding_df = df[df['key'].str.contains(corresponding_symbol, case=False, na=False)]
        if not corresponding_df.empty:
            corresponding_df = corresponding_df[['key', 'qty', 'PL%']].copy()
            # Merge the dataframes to calculate qty diff
            merged_df = filtered_df.merge(corresponding_df, left_on='key', right_on='key', suffixes=('', '_corresponding'))
            merged_df['qty diff'] = merged_df['qty'] - merged_df['qty_corresponding']
            merged_df['rebuy'] = ['Yes' if (row['qty'] < row['qty_corresponding'] and row['PL%'] < -5) else 'No' for _, row in merged_df.iterrows()]
            
            print(f"\nDetailed info for symbol '{symbol}':")
            print(merged_df[['key', 'qty', 'PL%', 'qty diff', 'rebuy']])
        else:
            print(f"No corresponding options found for symbol '{symbol}'.")
    else:
        print(f"No rows found for symbol '{symbol}'.")

try:
    sys.stdout = open('output.txt', 'w')
    broker = get_kite()
except Exception as e:
    remove_token(dir_path)
    print(traceback.format_exc())
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

# Check quantity for the provided symbol or ask user for input
if args.symbol:
    check_quantity_for_symbol(blnc_opt_df, args.symbol)
else:
    user_symbol = input("No symbol provided. Please enter a symbol to check: ").strip()
    check_quantity_for_symbol(blnc_opt_df, user_symbol)

