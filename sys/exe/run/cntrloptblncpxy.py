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

from clorpxy import RED, GREEN

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
        for index, row in blnc_opt_df.iterrows():
            total_pl_percentage = row['PL%']
            
            print(f"Checking conditions for {row['key']}: PL% = {total_pl_percentage}")
            if total_pl_percentage > row['Target']:
                print(f"Conditions met for {row['key']}, placing order")
                place_order(row['key'], row['qty'], 'SELL', 'MARKET', 'NRML', broker)
                message = (
                    f"🛬🛬🛬 😧😧😧 EXIT order placed {row['key']} successfully.\n"
                    f"🎯 Target PL%: {round(row['Target'], 4)}%\n"
                    f"🏆 Reached PL%: {round(total_pl_percentage, 2)}%\n"
                    f"💰 Booked Profit: {row['PnL']}\n"
                )
                print(message)
                send_telegram_message(message)
            else:
                print(f"Conditions not met for {row['key']}, skipping order")
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

# Get the next month's abbreviation
next_month_abbr = (datetime.now().replace(day=28) + timedelta(days=4)).strftime('%b').upper()  # e.g., 'JAN', 'FEB', 'MAR'

# Select only the key, qty, PL%, and PnL columns and filter by next month's abbreviation
filtered_df = blnc_opt_df[['key', 'qty', 'PL%', 'PnL']]
filtered_df = filtered_df[filtered_df['key'].str.contains(next_month_abbr)].copy()

print("Final DataFrame before calling exit_options:")
print(filtered_df.to_string(index=False))

# Call the function to exit options
exit_options(filtered_df, broker)

