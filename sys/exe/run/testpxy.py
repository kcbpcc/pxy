from datetime import datetime, timedelta
import numpy as np
import pandas as pd
from nsepy import get_expiry_date
from nsepy.derivatives import get_expiry_date

# Define the NIFTY index symbol
index_symbol = 'NIFTY'

# Determine next Thursday's date
today = datetime.today()
days_ahead = (3 - today.weekday() + 7) % 7  # Calculate days until next Thursday
next_thursday = today + timedelta(days=days_ahead)

# Get the expiry date for next week's Thursday
expiry_date = get_expiry_date(year=next_thursday.year, month=next_thursday.month)

# Get available option contracts for NIFTY expiring on the next Thursday
options = get_strike_prices(symbol=index_symbol, expiry_date=expiry_date, option_type='CE')

# Display the available option contracts
print("Options available for NIFTY expiring on", expiry_date)
print(options)
