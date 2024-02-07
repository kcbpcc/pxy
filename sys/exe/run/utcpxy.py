from datetime import datetime, timedelta

def calculate_cycle(current_time):
    # Define time intervals
    interval_1_start = datetime.strptime("03:45", "%H:%M").time()
    interval_1_end = datetime.strptime("04:00", "%H:%M").time()
    
    interval_2_start = datetime.strptime("09:45", "%H:%M").time()
    interval_2_end = datetime.strptime("10:00", "%H:%M").time()

    # Convert current time to datetime object with today's date
    current_datetime = datetime.combine(datetime.today(), current_time)

    # Check if current time is within the defined intervals
    if interval_1_start <= current_time <= interval_1_end:
        return "peakstart"
    elif interval_2_start <= current_time <= interval_2_end:
        return "peakend"
    else:
        # Check for non-peak time spanning midnight
        if interval_2_end < interval_2_start:  # Check if interval spans midnight
            if interval_2_end <= current_time or current_time <= interval_2_start:
                return "nonmkt"
        else:
            return "nonmkt"

# Get the current UTC time
current_utc_time = datetime.utcnow().time()

# Calculate status based on current time
status = calculate_cycle(current_utc_time)
print(status)
