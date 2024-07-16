import calendar
from datetime import datetime, timedelta

# List of public holidays
public_holidays = [
    "22-Jan-2024", "26-Jan-2024", "08-Mar-2024", "25-Mar-2024", "29-Mar-2024", 
    "11-Apr-2024", "17-Apr-2024", "01-May-2024", "20-May-2024", "17-Jun-2024", 
    "17-Jul-2024", "15-Aug-2024", "02-Oct-2024", "01-Nov-2024", "15-Nov-2024", 
    "25-Dec-2024"
]

# Convert the list of public holidays to datetime objects
public_holidays = [datetime.strptime(date, "%d-%b-%Y").date() for date in public_holidays]

def get_last_weekday_of_current_month(weekday):
    # Get the current date
    now = datetime.now()
    year = now.year
    month = now.month

    # Find the last day of the current month
    last_day = calendar.monthrange(year, month)[1]
    
    # Get the date of the last day of the month
    last_date = datetime(year, month, last_day)
    
    # Find the last specified weekday
    last_weekday = last_date - timedelta(days=(last_date.weekday() - weekday) % 7)
    
    # Adjust if the last weekday is a public holiday
    while last_weekday in public_holidays:
        last_weekday -= timedelta(days=1)
    
    return last_weekday.strftime("%m-%d")

# Get the last Wednesday and Thursday of the current month
last_wednesday = get_last_weekday_of_current_month(calendar.WEDNESDAY)
last_thursday = get_last_weekday_of_current_month(calendar.THURSDAY)

print(f"NIFTY Expiry {last_thursday} BANKNIFTY Expiry {last_wednesday}")


