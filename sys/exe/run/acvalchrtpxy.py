import pandas as pd
from asciichartpy import plot
from colorpxy import SILVER, BRIGHT_RED, BRIGHT_GREEN, RESET
from telsumrypxy import check_and_send_summary

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

# Create message
message = (
    f"{RESET}\n"
    f"{chart}\n"
    f"📊📊📊📊📊  Daily Delta: {delta_day_color}{delta_day:,.2f}{RESET}  📊📊📊📊📊\n"
    f"📊📊📊📊📊  Month Delta: {delta_month_color}{delta_month:,.2f}{RESET}  📊📊📊📊📊\n"
    f"{RESET}"
)

# Send message via check_and_send_summary
check_and_send_summary(message)

