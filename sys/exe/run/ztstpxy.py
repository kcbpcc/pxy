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
    if row['tradingsymbol'].startswith('BANKNIFTY'):
        return last_wednesday
    elif row['tradingsymbol'].startswith('NIFTY'):
        return last_thursday
    else:
        return None

def add_year_to_date(date_obj, year):
    if pd.isna(date_obj):
        return None
    return datetime(year, date_obj.month, date_obj.day).date()

def calculate_working_days(date_obj):
    if pd.isna(date_obj):
        return None
    try:
        current_date = datetime.now().date()
        return np.busday_count(date_obj, current_date)
    except Exception as e:
        print(f"Error calculating working days: {e}")
        return None

def send_telegram_message(message):
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

def exit_options(blnc_opt_df, broker):
    total_opt_pnl = calculate_totals(blnc_opt_df)
    try:
        for index, row in blnc_opt_df.iterrows():
            total_pl_percentage = row['PL%']
            tgtoptsmadepth = row['tgtoptsmadepth']
            
            if total_pl_percentage > tgtoptsmadepth and row['PnL'] > 400:
                place_order(row['key'], row['qty'], 'SELL', 'MARKET', 'NRML', broker)
                message = (
                    f"🛬🛬🛬 🎯🎯🎯 EXIT order placed {row['key']} successfully.\n"
                    f"🎯 Target PL%: {round(tgtoptsmadepth, 4)}%\n"
                    f"🏆 Reached PL%: {round(total_pl_percentage, 2)}%\n"
                    f"📉 Sell Price: {row['ltp']}\n"
                    f"📈 Buy Price: {row['avg']}\n"
                    f"💰 Booked Profit: {row['PnL']}\n"
                    f"Total Booked:💰 {total_opt_pnl} 📣"
                )
                print(message)
                send_telegram_message(message)
    except Exception as e:
        print(f"Error placing exit order: {e}")

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

# Add the 'Date' column
filtered_df['Date'] = filtered_df.apply(lambda row: add_year_to_date(add_date(row), current_year), axis=1)

# Calculate difference in working days between current date and Date
filtered_df['Days_Difference'] = filtered_df['Date'].apply(calculate_working_days)

# Reorder columns as requested
final_df = filtered_df[['tradingsymbol', 'Invested', 'value', 'PL%', 'Date', 'Days_Difference']]

print(final_df.to_string(index=False))

