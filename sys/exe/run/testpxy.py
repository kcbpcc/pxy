from toolkit.logger import Logger
from toolkit.currency import round_to_paise
from toolkit.utilities import Utilities
from login_get_kite import get_kite
from cnstpxy import dir_path, fileutils, buybuff, max_target
from buypluspxy import Trendlyne
import pandas as pd
import traceback
import sys
import os
from fundpxy import calculate_decision
decision = calculate_decision()
from mktpxy import get_market_check
onemincandlesequance, mktpxy = get_market_check()    
import asyncio
        try:
            broker = get_kite(api="bypass", sec_dir=dir_path)
        except Exception as e:
            remove_token(dir_path)
            print(traceback.format_exc())
            logging.error(f"{str(e)} unable to get holdings")
            sys.exit(1)

kite = broker['kite']

# Calculate the next Thursday date
current_date = datetime.now()
days_until_thursday = (3 - current_date.weekday() + 7) % 7  # Calculate days until next Thursday
expiry_date = current_date + timedelta(days=days_until_thursday)

# Format the date, month, and year
expiry_year = expiry_date.strftime("%y")
expiry_month = expiry_date.strftime("%m")
expiry_day = expiry_date.strftime("%d")

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

try:
    order_id = kite.place_order(
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
