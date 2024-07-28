import calendar
from datetime import datetime, timedelta

def get_last_weekday_of_current_month(weekday):
    today = datetime.today()
    year = today.year
    month = today.month
    
    # Find the last day of the current month
    last_day = calendar.monthrange(year, month)[1]
    last_date = datetime(year, month, last_day)
    
    # Find the last specified weekday of the current month
    while last_date.weekday() != weekday:
        last_date -= timedelta(days=1)
    
    # If the date is already in the past, move to the next month
    if last_date < today:
        # Move to the next month
        month += 1
        if month > 12:
            month = 1
            year += 1
        last_day = calendar.monthrange(year, month)[1]
        last_date = datetime(year, month, last_day)
        
        while last_date.weekday() != weekday:
            last_date -= timedelta(days=1)
    
    return last_date

# Get the last Wednesday and Thursday of the current month (or next month if already past)
last_wednesday = get_last_weekday_of_current_month(calendar.WEDNESDAY)
last_thursday = get_last_weekday_of_current_month(calendar.THURSDAY)

print("Last Wednesday:", last_wednesday)
print("Last Thursday:", last_thursday)
