import pandas as pd
from telsumrypxy import check_and_send_summary

# Load data from local CSV file
df = pd.read_csv('acvalpxy.csv')

# Convert 'date' column to datetime format if necessary
df['date'] = pd.to_datetime(df['date'])

# Consider the latest 30 records for calculations
df = df.tail(30)

# Calculate daily and monthly deltas
if len(df) >= 2:
    latest_record = df['acvalue'].iloc[-1]
    previous_record = df['acvalue'].iloc[-2]
    delta_day = latest_record - previous_record
else:
    delta_day = 0  # Default to 0 if not enough data

if len(df) >= 1:
    monthly_previous_record = df['acvalue'].iloc[0]
    delta_month = latest_record - monthly_previous_record
else:
    delta_month = delta_day  # Default to daily delta if not enough data

# Print deltas to console with zero-padding
print(f"📊📊📊📊📊   Daily Delta: {delta_day:0=6,.2f}  📊📊📊📊")
print(f"📊📊📊📊📊   Month Delta: {delta_month:0=6,.2f}  📊📊📊📊")

# Prepare the summary message for Telegram
telegram_message = (
    f"    🚀 *PXY® Score Board* 🚀\n\n"
    f"💰*Daily Delta:* {delta_day:0=6,.2f}\n\n"
    f"💰*Month Delta:* {delta_month:0=6,.2f}\n\n"   
    f"    🔗 [PXY® Dash Board](https://console.zerodha.com/verified/0aec4aa4)"
)

# Send the summary
check_and_send_summary(telegram_message, 'vlpxy')

