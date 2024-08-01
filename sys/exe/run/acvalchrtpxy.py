import pandas as pd
from telsumrypxy import check_and_send_summary

# Load data from local CSV file
df = pd.read_csv('acvalpxy.csv')

# Convert 'date' column to datetime format
df['date'] = pd.to_datetime(df['date'])

# Filter data for the past 14 days
end_date = df['date'].max()
start_date = end_date - pd.DateOffset(days=13)
df_filtered = df[(df['date'] >= start_date) & (df['date'] <= end_date)]

# Ensure data is sorted by date
df_filtered = df_filtered.sort_values(by='date')

# Calculate delta (Today - Yesterday)
df_filtered['delta'] = df_filtered['acvalue'].diff().fillna(0)

# Create the message
message_lines = ["Date       | AC Value | Delta"]
for _, row in df_filtered.iterrows():
    date_str = row['date'].strftime('%Y-%m-%d')
    ac_value_str = f"{row['acvalue']:,.2f}"
    delta_str = f"{row['delta']:,.2f}"
    message_lines.append(f"{date_str} | {ac_value_str} | {delta_str}")

message = "\n".join(message_lines)

# Source identifier
source = "accval"

# Send message via check_and_send_summary
check_and_send_summary(message, source)
