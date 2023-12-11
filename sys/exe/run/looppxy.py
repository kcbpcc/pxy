from datetime import datetime, timedelta

def calculate_loop_duration(current_time):
    # Define time intervals
    interval_1_start = datetime.strptime("03:44", "%H:%M").time()
    interval_1_end = datetime.strptime("04:00", "%H:%M").time()
    
    interval_2_start = datetime.strptime("09:14", "%H:%M").time()
    interval_2_end = datetime.strptime("09:44", "%H:%M").time()

    interval_3_start = datetime.strptime("09:45", "%H:%M").time()
    interval_3_end = datetime.strptime("03:43", "%H:%M").time()

    # Convert current time to time object
    current_time = current_time.time()

    # Check if current time is within the defined intervals
    if interval_1_start <= current_time <= interval_1_end or interval_2_start <= current_time <= interval_2_end:
        return 1
    elif interval_3_start <= current_time and current_time <= interval_3_end:
        # Calculate the remaining time until the end of interval_3
        remaining_time = timedelta(hours=12) - (current_time - interval_3_start)
        # Convert the remaining time to hours
        return round(remaining_time.total_seconds() / 3600)
    else:
        return 14

# Get the current UTC time
current_utc_time = datetime.utcnow()

# Calculate loop duration based on current time
loop_duration = calculate_loop_duration(current_utc_time)

print(f"Current UTC time: {current_utc_time.strftime('%H:%M')}")
print(f"Loop duration: {loop_duration} hours")
