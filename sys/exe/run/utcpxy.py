from datetime import datetime, timezone

def peak_time(utc_time):
    # Define the peak time ranges
    peak_start_1 = datetime.strptime("03:45", "%H:%M").replace(tzinfo=timezone.utc).time()
    peak_end_1 = datetime.strptime("04:00", "%H:%M").replace(tzinfo=timezone.utc).time()
    
    non_peak_start = datetime.strptime("04:00", "%H:%M").replace(tzinfo=timezone.utc).time()
    non_peak_end = datetime.strptime("09:45", "%H:%M").replace(tzinfo=timezone.utc).time()

    peak_start_2 = datetime.strptime("09:45", "%H:%M").replace(tzinfo=timezone.utc).time()
    peak_end_2 = datetime.strptime("10:00", "%H:%M").replace(tzinfo=timezone.utc).time()

    # Check if the current time is within the peak time ranges
    if peak_start_1 <= utc_time < peak_end_1:
        return "peakstart"
    elif non_peak_start <= utc_time < non_peak_end:
        return "nonpeak"
    elif peak_start_2 <= utc_time < peak_end_2:
        return "peakend"
    else:
        return "nonmkt"

# Get the current UTC time
current_utc_time = datetime.utcnow().replace(tzinfo=timezone.utc).time()

print(peak_time(current_utc_time))

