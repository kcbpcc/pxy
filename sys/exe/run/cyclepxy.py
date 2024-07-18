from datetime import datetime, timedelta

def calculate_cycle(current_time):
    # Define time intervals
    interval_1_start = datetime.strptime("03:30", "%H:%M").time()
    interval_1_end = datetime.strptime("04:15", "%H:%M").time()
    
    interval_2_start = datetime.strptime("09:15", "%H:%M").time()
    interval_2_end = datetime.strptime("10:00", "%H:%M").time()

    interval_3_start = datetime.strptime("10:00", "%H:%M").time()
    interval_3_end = datetime.strptime("03:40", "%H:%M").time()

    # Convert current time to datetime object with today's date
    current_datetime = datetime.combine(datetime.today(), current_time)

    # Check if current time is within the defined intervals
    if interval_1_start <= current_time <= interval_1_end or interval_2_start <= current_time <= interval_2_end:
        return 6
    elif interval_3_start <= current_time or current_time <= interval_3_end:
        # Convert interval end times to datetime objects
        interval_3_start_datetime = datetime.combine(datetime.today(), interval_3_start)
        interval_3_end_datetime = datetime.combine(datetime.today(), interval_3_end)

        # Calculate the time remaining until the end of interval_3
        remaining_time = (interval_3_end_datetime - current_datetime) if current_datetime <= interval_3_end_datetime else (timedelta(days=1) + interval_3_end_datetime - current_datetime)
        remaining_time /= 4

        # Convert the remaining time to seconds
        return round(remaining_time.total_seconds())
    else:
        return 6

# Get the current UTC time
current_utc_time = datetime.utcnow().time()

# Calculate loop duration based on current time
cycle = calculate_cycle(current_utc_time)
#print(f"Current UTC time: {current_utc_time.strftime('%H:%M')}".rjust(40))
#print(f"...lets fire again 🚀 🚀 🚀 Cycle 🎡 : {cycle} seconds".rjust(40))
