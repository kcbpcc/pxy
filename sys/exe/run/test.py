import locale
from datetime import datetime, timezone, timedelta

# Set the IST timezone
ist_timezone = timezone(timedelta(hours=5, minutes=30))

# Set Telugu locale
locale.setlocale(locale.LC_TIME, 'te_IN')

# Get current date and time in IST
current_datetime_ist = datetime.now(ist_timezone)

# Format the date and time
formatted_datetime_ist = current_datetime_ist.strftime("%Y-%m-%d %H:%M:%S")

# Get the day in Telugu
day_of_week_ist_telugu = current_datetime_ist.strftime("%A")

# Display the information
print("Current Date and Time (IST):", formatted_datetime_ist)
print("Day of the Week (IST):", day_of_week_ist_telugu)