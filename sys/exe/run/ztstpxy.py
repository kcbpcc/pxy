import pandas as pd
import numpy as np
from datetime import datetime
import calendar
from expdaypxy import get_last_weekday_of_current_month

# Define function to get last weekday dates
last_wednesday = get_last_weekday_of_current_month(calendar.WEDNESDAY)
last_thursday = get_last_weekday_of_current_month(calendar.THURSDAY)

# Dummy data for demonstration (Replace this with actual DataFrame)
data = {
    'tradingsymbol': ['BANKNIFTY24JUL52500CE', 'BANKNIFTY24JUL53100CE', 'BANKNIFTY24JUL53200CE'],
    'Invested': [14036, 15635, 14130],
    'value': [568.50, 195.00, 153.75],
    'PL%': [-95.946139, -98.752798, -98.910120],
}

filtered_df = pd.DataFrame(data)

# Add the 'Date' column based on trading symbol
def add_date(row):
    if row['tradingsymbol'].startswith('BANKNIFTY'):
        return last_wednesday
    elif row['tradingsymbol'].startswith('NIFTY'):
        return last_thursday
    else:
        return None

filtered_df.loc[:, 'Date'] = filtered_df.apply(add_date, axis=1)

# Calculate difference in working days between current date and Date
def calculate_working_days(date_obj):
    if pd.isna(date_obj):
        return None
    try:
        current_date = datetime.now().date()
        return np.busday_count(date_obj, current_date)
    except Exception as e:
        print(f"Error calculating working days: {e}")
        return None

# Ensure 'Date' is in datetime format before applying the function
filtered_df['Date'] = pd.to_datetime(filtered_df['Date'], format='%d-%b', errors='coerce').dt.date

# Apply the working days calculation
filtered_df.loc[:, 'Days_Difference'] = filtered_df['Date'].apply(calculate_working_days)

# Reorder columns as requested
final_df = filtered_df[['tradingsymbol', 'Invested', 'value', 'PL%', 'Date', 'Days_Difference']]

print(final_df.to_string(index=False))

