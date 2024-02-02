from datetime import datetime, timedelta
from toolkit.logger import Logger
from toolkit.currency import round_to_paise
from toolkit.utilities import Utilities
from login_get_kite import get_kite, remove_token
from cnstpxy import dir_path, fileutils, buybuff, max_target
from buypluspxy import Trendlyne
import pandas as pd
import traceback
import sys
import os
from fundpxy import calculate_decision
from nftpxy import OPTIONS
import time 

decision = calculate_decision()
from mktpxy import get_market_check

onemincandlesequance, mktpxy = get_market_check()

try:
    broker = get_kite(api="bypass", sec_dir=dir_path)
except Exception as e:
    remove_token(dir_path)
    print(traceback.format_exc())
    logging.error(f"{str(e)} unable to get holdings")
    sys.exit(1)

# Ensure that the 'broker' object has an 'order_place' method
if not hasattr(broker, 'order_place') or not callable(getattr(broker, 'order_place', None)):
    print("Error: 'broker' object does not have 'order_place' method.")
    sys.exit(1)

# Calculate the next Thursday date at least 6 days ahead
current_date = datetime.now()
days_until_next_thursday = (3 - current_date.weekday() + 7) % 7

# Ensure at least 6 days ahead
if days_until_next_thursday < 6:
    days_until_next_thursday += 7

next_thursday = current_date + timedelta(days=days_until_next_thursday)

# Format the date, month, and year
expiry_year = next_thursday.strftime("%y")
expiry_month = next_thursday.strftime("%m")
expiry_day = next_thursday.strftime("%d")

# Ensure the month is one digit until October
if int(expiry_month) < 10:
    expiry_month = expiry_month[1]

# Ensure the date is always two digits
expiry_day = expiry_day.zfill(2)

# Construct the symbol for the NIFTY Put Option
symbol = f"NIFTY{expiry_year}{expiry_month}{expiry_day}{OPTIONS}PE"

quantity = 50  # Change this to the desired quantity
transaction_type = "BUY_TO_OPEN"  # For buying a put option to open a new position
order_type = "MARKET"
product_type = "NRML"  # For overnight/position trading

print("Symbol:", symbol)

# Get user confirmation
user_confirmation = input("Do you want to proceed? (Y/N): ").upper()

user_confirmation = input("Do you want to proceed? (Y/N): ").upper()

if user_confirmation == 'Y':
    try:
        order_id = broker.order_place(
            tradingsymbol=symbol,
            quantity=quantity,
            exchange="NFO",
            transaction_type=transaction_type,
            order_type=order_type,
            product=product_type
        )

        print("Order placed successfully. Order ID:", order_id)

    except Exception as e:
        print("Error placing order:", e)

else:
    print("Waiting for 10 seconds and then exiting...")
    time.sleep(10)  # Sleep for 10 seconds
    sys.exit(0)  # Exit the program
