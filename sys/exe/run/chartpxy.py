import pandas as pd
from asciichartpy import plot
from clorpxy import SILVER, BRIGHT_RED, BRIGHT_GREEN, RESET
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Reset terminal color to default
print(RESET)

# Define the scope and credentials for Google Sheets API
SCOPES = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('accvalue.json', SCOPES)

# Authorize the client using the credentials
client = gspread.authorize(creds)

# Open the Google Sheets document by its title
sheet = client.open('accvalue').sheet1

# Get all records from the Google Sheet
data = sheet.get_all_records()

# Convert the data to a DataFrame
df = pd.DataFrame(data)

# Convert 'date' column to datetime format
df['date'] = pd.to_datetime(df['date'])

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

# Adjust the ASCII chart to show weekly and daily intervals
weekly_length = 40
daily_length = 20

# Split chart into lines and format accordingly
lines = chart.split('\n')
for line in lines:
    # Ensure weekly part
    if len(line) >= weekly_length:
        weekly_part = line[:weekly_length]
    else:
        weekly_part = line.ljust(weekly_length)

    # Ensure daily part
    if len(line) > weekly_length:
        daily_part = line[weekly_length:weekly_length + daily_length]
    else:
        daily_part = ""

    # Print formatted line
    print(f"{weekly_part.ljust(weekly_length)} {daily_part}")

# Calculate delta
latest_record = df['acvalue'].iloc[-1]
previous_record = df['acvalue'].iloc[-2]
delta = int((latest_record - previous_record) * 100000)
delta_color = BRIGHT_GREEN if delta >= 0 else BRIGHT_RED

# Print delta
print("📊📊📊📊📊📊 Delta: {}{}📊📊📊📊📊📊".format(delta_color, str(delta).zfill(10)))

# Reset terminal color to default
print(RESET)




