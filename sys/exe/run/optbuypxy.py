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
import select


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
# Construct the symbol for the NIFTY Put Option
symbol_PE = f"NIFTY{expiry_year}{expiry_month}{expiry_day}{OPTIONS}PE"
symbol_CE = f"NIFTY{expiry_year}{expiry_month}{expiry_day}{OPTIONS}CE"
#print("Do you want to execute", symbol_CE, symbol_PE)

# Get user confirmation
print("Do you want to execute", symbol_CE, symbol_PE)
start_time = time.time()
user_confirmation = ''
while time.time() - start_time < 120:
    rlist, _, _ = select.select([sys.stdin], [], [], 0.1)  # Check for input every 0.1 seconds
    if rlist:
        user_confirmation = sys.stdin.read(1).upper()
        break

if not user_confirmation:
    user_confirmation = 'N'

if user_confirmation == 'Y':
    try:
        order_id_PE = broker.order_place(
            tradingsymbol=symbol_PE,
            quantity=50,
            exchange="NFO",
            transaction_type='BUY',
            order_type='MARKET',
            product='MIS'
        )
        order_id_CE = broker.order_place(
            tradingsymbol=symbol_CE,
            quantity=50,
            exchange="NFO",
            transaction_type='BUY',
            order_type='MARKET',
            product='MIS'
        )

        print("Orders placed successfully. Order IDs:", order_id_PE, order_id_CE)

    except Exception as e:
        print("Error placing order:", e)

else:
    print("Operation cancelled by user. Exiting...")
    time.sleep(10)  # Sleep for 10 seconds
    sys.exit(0)  # Exit the program

