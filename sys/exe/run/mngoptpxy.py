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
def get_last_weekday_dates():
    last_wednesday = get_last_weekday_of_current_month(calendar.WEDNESDAY)
    last_thursday = get_last_weekday_of_current_month(calendar.THURSDAY)
    return last_wednesday, last_thursday

# Get the current year
current_year = datetime.now().year
now = datetime.now()
current_month_abbr = now.strftime('%b')

def parse_date(date_str):
    return datetime.strptime(f"{date_str}-{current_year}", '%d-%b-%Y')

last_wednesday_str, last_thursday_str = get_last_weekday_dates()
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
            response.raise_for_status()  # Raise an exception for HTTP errors
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
            if row['PL%'] > row['Target']:
                place_order(row['key'], row['qty'], 'SELL', 'MARKET', 'NRML', broker)
                message = (
                    f"🛬🛬🛬 😧😧😧 EXIT order placed {row['key']} successfully.\n"
                    f"🎯 Target PL%: {round(row['Target'], 4)}%\n"
                    f"🏆 Reached PL%: {round(row['PL%'], 2)}%\n"
                    f"💰 Booked Profit: {row['PnL']}\n"
                )
                print(message)
                send_telegram_message(message)
    except Exception as e:
        print(f"Error placing exit order: {e}")

def place_buy_orders_based_on_pl(final_avg_df, broker):
    try:
        for index, row in final_avg_df.iterrows():
            if row['PL%'] < -66:
                # Create orders based on the row data
                strike_price = int(row['key'].split('-')[-1])
                if 'CE' in row['key']:
                    order_strikes = [strike_price + 100, strike_price + 200]
                elif 'PE' in row['key']:
                    order_strikes = [strike_price - 100, strike_price - 200]
                else:
                    continue

                for strike in order_strikes:
                    symbol = f"NIFTY{current_year % 100}{(now.month % 12) + 1:02d}{strike}"
                    place_order(symbol, row['qty'], 'BUY', 'MARKET', 'NRML', broker)
                    print(f"Placed BUY order for {symbol} with quantity {row['qty']}.")
    except Exception as e:
        print(f"Error placing buy orders: {e}")

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

# Debugging: Print combined_df
print("Combined DataFrame:")
print(combined_df.head())

blnc_opt_df = combined_df[
    (combined_df['key'].str.contains('NFO:', case=False, na=False)) &
    (combined_df['qty'] > 0) &
    (combined_df['key'].notna())
].copy()

# Debugging: Print blnc_opt_df
print("Filtered blnc_opt_df:")
print(blnc_opt_df.head())

blnc_opt_df['key'] = blnc_opt_df['key'].str.replace('NFO:', '', regex=False)
blnc_opt_df['PL%'] = (blnc_opt_df['PnL'] / blnc_opt_df['Invested']) * 100
blnc_opt_df['PL%'] = blnc_opt_df['PL%'].fillna(0)

blnc_opt_df['strike'] = blnc_opt_df['key'].str.replace(r'(PE|CE)$', '', regex=True)

# Filter based on PL%
blnc_opt_df = blnc_opt_df[blnc_opt_df['PL%'] < -66]

# Debugging: Print filtered blnc_opt_df
print("Filtered blnc_opt_df after PL% < -66:")
print(blnc_opt_df.head())

blnc_opt_df['Date'] = blnc_opt_df['key'].apply(lambda key: last_wednesday if key.startswith('BANKNIFTY') else (last_thursday if key.startswith('NIFTY') else None))
blnc_opt_df['Today'] = datetime.now()
blnc_opt_df['Diff'] = blnc_opt_df.apply(lambda row: business_days_diff(row['Date'], row['Today']) if pd.notna(row['Date']) else None, axis=1)

blnc_opt_df['Date'] = blnc_opt_df['Date'].dt.day
blnc_opt_df['Today'] = blnc_opt_df['Today'].dt.day

blnc_opt_df['Target'] = blnc_opt_df['Diff'].apply(lambda x: (100 - (x * 9)) * -1 if x < 10 else 107)
blnc_opt_df = blnc_opt_df[blnc_opt_df['qty'] > 0]

# Debugging: Print final DataFrame
print("Final DataFrame for exit and buy orders:")
print(blnc_opt_df.head())

# Create final_df with appropriate filter
final_df = blnc_opt_df[blnc_opt_df['Target'] < 0][['key', 'qty', 'Invested', 'value', 'PL%', 'PnL', 'Date', 'Today', 'Diff', 'Target']]

# Debugging: Print final_df
print("Final DataFrame:")
print(final_df.head())

row_count = final_df.shape[0]
sum_invested = final_df['Invested'].sum()

# Print data
width = 42
line1 = f"B:{last_wednesday_str}"
line2 = f"N:{last_thursday_str}"

print("━" * 42)
combined_lines = f"{line1} ⚖     {BRIGHT_YELLOW}INVESTED:{RESET} {sum_invested:.2f}"
print(f"{combined_lines: <{width}}")
print(f"{line2: <{width}}")

try:
    # Exit and Buy orders
    exit_options(final_df, broker)
    place_buy_orders_based_on_pl(final_df, broker)
except Exception as e:
    print(f"Error during processing: {e}")

# Ensure final debug output
print("Final DataFrame after processing:")
print(final_df.head())

