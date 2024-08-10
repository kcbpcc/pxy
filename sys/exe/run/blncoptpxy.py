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
parser.add_argument('command', nargs='?', choices=['l', 's'], default='s',
                    help="Command to run the program with. Defaults to 's' if not provided.")
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
        #print(f"Placing order for {tradingsymbol} with quantity {quantity}")
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

def avg_options(df, broker):
    try:
        for index, row in df.iterrows():
            qty = 0
            can_average = False

            print(f"\nProcessing row {index + 1}:")
            print(f"Key: {row['key']}")
            print(f"Quantity: {row['qty']}")
            print(f"PnL: {row['PnL']}")
            print(f"PL%: {row['PL%']}%")

            if row['key'].startswith('BANKNIFTY'):
                current_qty = row['qty']
                if current_qty < 30:
                    qty = 15
                    if 'PE' in row['key']:
                        can_average = (bnk_power > 0.90)
                        if not can_average:
                            print("Cannot average: bnk_power <= 0.90")
                    elif 'CE' in row['key']:
                        can_average = (bnk_power < 0.10)
                        if not can_average:
                            print("Cannot average: bnk_power >= 0.10")
                else:
                    print(f"Quantity {current_qty} >= 30, skipping averaging.")

            elif row['key'].startswith('NIFTY'):
                current_qty = row['qty']
                if current_qty < 50:
                    qty = 25
                    if 'PE' in row['key']:
                        can_average = (nse_power > 0.90)
                        if not can_average:
                            print("Cannot average: nse_power <= 0.90")
                    elif 'CE' in row['key']:
                        can_average = (nse_power < 0.10)
                        if not can_average:
                            print("Cannot average: nse_power >= 0.10")
                else:
                    print(f"Quantity {current_qty} >= 50, skipping averaging.")

            if can_average:
                while True:
                    try:
                        user_input = input("May I place an order? (Yes/No): ").strip()
                        if user_input in ('Yes', 'No'):
                            break
                        print("Invalid input. Please enter 'Yes' or 'No'.")
                    except EOFError:
                        print("Error reading input. Please try again.")
                        continue

                if user_input == 'Yes':
                    order_id = place_order(row['key'], qty, 'BUY', 'MARKET', 'NRML', broker)
                    if order_id:
                        message = (
                            f"🚀🚀🚀 🤑🤑🤑 AVG order placed {row['key']} successfully.\n"
                            f"PL%: {round(row['PL%'], 2)}%\n"
                            f"Quantity: {qty}\n"
                        )
                        print(message)
                        send_telegram_message(message)
                else:
                    print("User chose not to place an order.")
            else:
                print(f"{BRIGHT_GREEN}Skipping order: conditions not met.{RESET}")

    except Exception as e:
        print(f"Error processing row: {e}")




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

blnc_opt_df['strike'] = blnc_opt_df['key'].str.replace(r'(PE|CE)$', '', regex=True)

current_month_abbr = datetime.now().strftime('%b').upper()

blnc_opt_df = blnc_opt_df[['key', 'qty', 'Invested', 'value', 'PL%', 'PnL']]
blnc_opt_df = blnc_opt_df[blnc_opt_df['qty'] > 0]
total_invested = blnc_opt_df['Invested'].sum() if not blnc_opt_df.empty else 0
# Apply additional filtering conditions
blnc_opt_df = blnc_opt_df[
    ((blnc_opt_df['key'].str.startswith('BANK')) & (blnc_opt_df['qty'] < 30)) |
    ((blnc_opt_df['key'].str.startswith('NIFTY')) & (blnc_opt_df['qty'] < 50))
]
#blnc_opt_df = blnc_opt_df[blnc_opt_df['key'].str.contains(current_month_abbr)]

def add_date(row):
    if row['key'].startswith('BANKNIFTY'):
        return last_wednesday
    elif row['key'].startswith('NIFTY'):
        return last_thursday
    else:
        return None

blnc_opt_df['Date'] = blnc_opt_df.apply(add_date, axis=1)
blnc_opt_df['Today'] = datetime.now()

blnc_opt_df['Diff'] = blnc_opt_df.apply(lambda row: business_days_diff(row['Date'], row['Today']), axis=1)

blnc_opt_df['Date'] = blnc_opt_df['Date'].dt.day
blnc_opt_df['Today'] = blnc_opt_df['Today'].dt.day

blnc_opt_df['Target'] = blnc_opt_df['Diff'].apply(lambda x: (100 - (x * 9)) * -1 if x < 10 else 107)

# Define width for formatting
width = 42

# Calculate total invested


# Define colors based on specific conditions for each line
if bnk_power > 0.85 or bnk_power < 0.15:
    line1_color = SILVER
else:
    line1_color = GREY

if nse_power > 0.85 or nse_power < 0.15:
    line2_color = SILVER
else:
    line2_color = GREY

# Format lines with the defined colors
line1 = f"{line1_color}B:{last_wednesday_str}{RESET}"
line2 = f"{line2_color}N:{last_thursday_str}{RESET}"
formatted_total = f"{total_invested:07d}"

# Construct header line with colored lines
header_line = f"{line1}  ⚖    {BRIGHT_YELLOW}{current_month_abbr}{RESET}  {formatted_total}   ⚖   {line2}"

# Print border
print("━" * width)

# Print header line centered
print(f"{header_line:^{width}}")


avg_nifty_df = blnc_opt_df[
    (blnc_opt_df['PL%'] < -33) &
    (blnc_opt_df['key'].str.startswith('NIFTY'))
]

print(avg_nifty_df[['key', 'qty', 'PL%']].to_string(index=False, header=False, formatters={'key': lambda x: f"{x:<28}", 'qty': lambda x: f"{x:>6}", 'PL%': lambda x: f"{x:>6.2f}"}))

avg_bnk_nifty_df = blnc_opt_df[
    (blnc_opt_df['PL%'] < -33) &
    (blnc_opt_df['key'].str.startswith('BANKNIFTY'))
]

print(avg_bnk_nifty_df[['key', 'qty', 'PL%']].to_string(index=False, header=False, formatters={'key': lambda x: f"{x:<28}", 'qty': lambda x: f"{x:>6}", 'PL%': lambda x: f"{x:>6.2f}"}))

avg_options(avg_nifty_df , broker)
avg_options(avg_bnk_nifty_df , broker)
