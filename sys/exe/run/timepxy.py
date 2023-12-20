import datetime
import pytz

def calculate_timpxy():
    # Define the start time in UTC
    start_time_utc = datetime.datetime.utcnow().replace(hour=3, minute=20, second=0, microsecond=0, tzinfo=pytz.utc)
    
    # Define the end time in UTC
    end_time_utc = datetime.datetime.utcnow().replace(hour=9, minute=30, second=0, microsecond=0, tzinfo=pytz.utc)

    # Get the current date and time in UTC
    current_datetime_utc = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)

    # Calculate timpxy value based on the minute difference in UTC
    if start_time_utc <= current_datetime_utc <= end_time_utc:
        total_minutes = (current_datetime_utc - start_time_utc).total_seconds() / 60
        total_time_range_minutes = (end_time_utc - start_time_utc).total_seconds() / 60
        
        # Calculate timpxy using linear interpolation
        timpxy = max(7, round(14 - (total_minutes / total_time_range_minutes) * 7, 2))
        return timpxy
    else:
        # Return 7 for all times outside the specified time range
        return 7

# Example usage:
result = calculate_timpxy()
print(f"PXY® is running on timepxy ⏰ {result} ⏰")
print(" " * 42)
