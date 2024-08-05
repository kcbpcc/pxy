import pandas as pd
from asciichartpy import plot
from clorpxy import SILVER, BRIGHT_RED, BRIGHT_GREEN, RESET
from telsumrypxy import check_and_send_summary

# Reset terminal color to default
print(RESET)

# Load data from local CSV file
df = pd.read_csv('acvalpxy.csv')

# Convert 'date' column to datetime format if necessary
df['date'] = pd.to_datetime(df['date'])

# Consider the latest 30 records for charting
df = df.tail(30)

# Calculate trend direction
trend_direction = []
for i in range(1, len(df)):
    if df['acvalue'][i] > df['acvalue'][i - 1]:
        trend_direction.append(BRIGHT_GREEN)
    elif df['acvalue'][i] < df['acvalue'][i - 1]:
        trend_direction.append(BRIGHT_RED)
    else:
        trend_direction.append(SILVER)

# Create ASCII chart with colored trend
chart = plot(df['acvalue'].tolist(), {'height': 10, 'format': "{:,.2f}", 'color': trend_direction})

# Adjust the ASCII chart to show monthly, weekly, and daily intervals
monthly_length = 12
weekly_length = 12
daily_length = 12

# Split chart into lines and format accordingly
lines = chart.split('\n')
for line in lines:
    # Ensure monthly part
    if len(line) >= monthly_length:
        monthly_part = line[:monthly_length]
    else:
        monthly_part = line.ljust(monthly_length)

    # Ensure weekly part
    if len(line) >= monthly_length + weekly_length:
        weekly_part = line[monthly_length:monthly_length + weekly_length]
    else:
        weekly_part = line[monthly_length:].ljust(weekly_length)

    # Ensure daily part
    if len(line) > monthly_length + weekly_length:
        daily_part = line[monthly_length + weekly_length:]
    else:
        daily_part = ""

    # Print formatted line with maximum 20 characters
    print(f"{monthly_part.ljust(monthly_length)} {weekly_part.ljust(weekly_length)} {daily_part[:daily_length]}")

# Calculate deltas
latest_record = df['acvalue'].iloc[-1]
previous_record = df['acvalue'].iloc[-2]
delta_day = latest_record - previous_record

# Monthly delta calculation
if len(df) > 1:
    monthly_previous_record = df['acvalue'].iloc[0]
    delta_month = latest_record - monthly_previous_record
else:
    delta_month = delta_day  # Not enough data for a full month delta

# Format deltas
delta_day_color = BRIGHT_GREEN if delta_day >= 0 else BRIGHT_RED
delta_month_color = BRIGHT_GREEN if delta_month >= 0 else BRIGHT_RED

# Print deltas to console with zero-padding
print(f"📊📊📊📊📊   Daily Delta: {delta_day:0=6,.2f}  📊📊📊📊")
print(f"🎢🎢🎢🎢🎢   Month Delta: {delta_month:0=6,.2f}  🎢🎢🎢🎢")

# Reset terminal color to default
print(RESET)


telegram_message = (
    f"    🚀 *PXY® Score Board* 🚀\n\n"
    f"💰*Daily Delta:* {delta_day:,.2f}\n\n"
    f"💰*Month Delta:* {delta_month:,.2f}\n\n"   
    f"    🔗 [PXY® Dash Board](https://console.zerodha.com/verified/0aec4aa4)"
)

# Print detailed entries to console
#print("\nDetailed Entries Preview:\n")
#print(telegram_message)

# Send the summary
check_and_send_summary(telegram_message, 'vlpxy')
