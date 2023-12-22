from datetime import datetime, timezone

def peak_time():
    # Get the current UTC time
    utc_time = datetime.utcnow().replace(tzinfo=timezone.utc)

    # Define the peak time ranges
    peak_time_1_start = datetime.strptime("03:45", "%H:%M").replace(tzinfo=timezone.utc)
    peak_time_1_end = datetime.strptime("04:00", "%H:%M").replace(tzinfo=timezone.utc)
    
    peak_time_2_start = datetime.strptime("09:45", "%H:%M").replace(tzinfo=timezone.utc)
    peak_time_2_end = datetime.strptime("10:00", "%H:%M").replace(tzinfo=timezone.utc)

    # Check if the current time is within the peak time ranges
    peak = (peak_time_1_start <= utc_time <= peak_time_1_end) or \
              (peak_time_2_start <= utc_time <= peak_time_2_end)

    return peak

if __name__ == "__main__":
    if peak_time():
        print("It's peak time!")
    else:
        print("It's not peak time.")
