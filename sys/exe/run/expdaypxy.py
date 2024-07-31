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

def get_last_weekday_of_month(year, month, weekday):
    # Find the last day of the month
    last_day = calendar.monthrange(year, month)[1]
    last_date = datetime(year, month, last_day)
    
    # Find the last specified weekday of the month
    while last_date.weekday() != weekday:
        last_date -= timedelta(days=1)
    
    # Adjust if the last weekday is a public holiday
    while last_date.date() in public_holidays or last_date.weekday() >= 5:
        last_date -= timedelta(days=1)
    
    return last_date

def get_last_weekday_of_current_month(weekday):
    # Get the current date
    now = datetime.now()
    year = now.year
    month = now.month

    # Find the last weekday for the current month
    last_weekday = get_last_weekday_of_month(year, month, weekday)
    
    # If the last weekday is in the past, find it for the next month
    if last_weekday < datetime(year, month, now.day):
        month += 1
        if month > 12:
            month = 1
            year += 1
        last_weekday = get_last_weekday_of_month(year, month, weekday)
    
    return last_weekday.strftime("%d-%b").upper()

# Get the last Wednesday and Thursday of the current month (or next month if already past)
last_wednesday = get_last_weekday_of_current_month(2)  # Wednesday is 2
last_thursday = get_last_weekday_of_current_month(3)   # Thursday is 3




