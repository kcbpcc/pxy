import datetime
import pytz

def calculate_timpxy():
    # Define the start time in UTC
    start_time_utc = datetime.datetime.utcnow().replace(hour=3, minute=30, second=0, microsecond=0, tzinfo=pytz.utc)
    
    # Define the end time in UTC
    end_time_utc = datetime.datetime.utcnow().replace(hour=9, minute=30, second=0, microsecond=0, tzinfo=pytz.utc)

    # Get the current date and time in UTC
    current_datetime_utc = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)

    # Calculate timpxy value based on the minute difference in UTC
    if start_time_utc <= current_datetime_utc <= end_time_utc:
        total_minutes = (current_datetime_utc - start_time_utc).total_seconds() / 60
        timpxy = max(5, round(18 - total_minutes / 30, 1))
        return timpxy
    else:
        # Return 5 for all times outside the specified time range
        return 5

# Example usage:
result = calculate_timpxy()
#print(result)
