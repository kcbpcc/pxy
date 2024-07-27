import calendar
from datetime import datetime, timedelta
from clorpxy import SILVER, UNDERLINE, RESET, BRIGHT_YELLOW, BRIGHT_RED, BRIGHT_GREEN, BOLD, GREY

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

    def find_last_weekday(year, month, weekday):
        # Find the last day of the month
        last_day = calendar.monthrange(year, month)[1]
        last_date = datetime(year, month, last_day)
        
        # Find the last specified weekday of the month
        last_weekday = last_date - timedelta(days=(last_date.weekday() - weekday) % 7)
        
        # Adjust if the last weekday is a public holiday
        while last_weekday.date() in public_holidays:
            last_weekday -= timedelta(days=1)
        
        return last_weekday

    # Find the last weekday for the current month
    last_weekday = find_last_weekday(year, month, weekday)
    
    # If the last weekday is in the past, move to the next month
    if last_weekday < now:
        month += 1
        if month > 12:
            month = 1
            year += 1
        last_weekday = find_last_weekday(year, month, weekday)
    
    return last_weekday

# Get the last Wednesday and Thursday of the current month (or next month if already past)
last_wednesday = get_last_weekday_of_current_month(calendar.WEDNESDAY)
last_thursday = get_last_weekday_of_current_month(calendar.THURSDAY)

# Print the values
print(f"Last Wednesday: {last_wednesday.strftime('%d-%b').upper()} ({last_wednesday})")
print(f"Last Thursday: {last_thursday.strftime('%d-%b').upper()} ({last_thursday})")

print(f"Last Thursday: {last_thursday}")

