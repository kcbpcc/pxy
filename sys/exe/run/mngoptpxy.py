import sys
import pandas as pd
from datetime import datetime
import calendar
from expdaypxy import get_last_weekday_of_current_month

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

# Process data and create DataFrame
combined_df = process_data()

# Debugging: Print combined_df
print("Combined DataFrame:")
print(combined_df.head())

# Filter DataFrame
blnc_opt_df = combined_df[
    (combined_df['key'].str.contains('NFO:', case=False, na=False)) &
    (combined_df['qty'] > 0) &
    (combined_df['key'].notna())
].copy()

# Debugging: Print blnc_opt_df
print("Filtered blnc_opt_df:")
print(blnc_opt_df.head())

# Clean and compute additional columns
blnc_opt_df['key'] = blnc_opt_df['key'].str.replace('NFO:', '', regex=False)
blnc_opt_df['PL%'] = (blnc_opt_df['PnL'] / blnc_opt_df['Invested']) * 100
blnc_opt_df['PL%'] = blnc_opt_df['PL%'].fillna(0)

blnc_opt_df['strike'] = blnc_opt_df['key'].str.replace(r'(PE|CE)$', '', regex=True)

# Calculate additional columns
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

# Print summary data
width = 42
line1 = f"B:{last_wednesday_str}"
line2 = f"N:{last_thursday_str}"

print("━" * 42)
combined_lines = f"{line1} ⚖     {BRIGHT_YELLOW}INVESTED:{RESET} {final_df['Invested'].sum():.2f}"
print(f"{combined_lines: <{width}}")
print(f"{line2: <{width}}")

# Ensure final debug output
print("Final DataFrame after processing:")
print(final_df.head())

# Filter DataFrames
df_target_positive = final_df[final_df['Target'] > 0][['key', 'qty', 'Invested', 'value', 'PL%', 'PnL', 'Date', 'Target']]
df_target_negative = final_df[final_df['Target'] < 0][['key', 'qty', 'Invested', 'value', 'PL%', 'PnL', 'Date', 'Target']]

# Print DataFrames
print("DataFrame with Target > 0:")
print(df_target_positive)

print("\nDataFrame with Target < 0:")
print(df_target_negative)

