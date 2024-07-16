import calendar
from datetime import datetime, timedelta

def get_last_wednesday_of_current_month():
    # Get the current date
    now = datetime.now()
    year = now.year
    month = now.month

    # Find the last day of the current month
    last_day = calendar.monthrange(year, month)[1]
    
    # Get the date of the last day of the month
    last_date = datetime(year, month, last_day)
    
    # Find the last Wednesday
    last_wednesday = last_date - timedelta(days=(last_date.weekday() - calendar.WEDNESDAY) % 7)
    
    return last_wednesday.date()

# Get the last Wednesday of the current month
last_wednesday = get_last_wednesday_of_current_month()
print("The last Wednesday of the current month is:", last_wednesday)
