from datetime import datetime, timezone

def peak_time():
    # Get the current UTC time
    utc_time = datetime.utcnow().replace(tzinfo=timezone.utc)

    # Define the peak time ranges
    peak_start_1 = datetime.strptime("03:45", "%H:%M").replace(tzinfo=timezone.utc)
    peak_end_1 = datetime.strptime("04:00", "%H:%M").replace(tzinfo=timezone.utc)
    
    non_peak_start = datetime.strptime("04:00", "%H:%M").replace(tzinfo=timezone.utc)
    non_peak_end = datetime.strptime("09:45", "%H:%M").replace(tzinfo=timezone.utc)

    peak_start_2 = datetime.strptime("09:45", "%H:%M").replace(tzinfo=timezone.utc)
    peak_end_2 = datetime.strptime("10:00", "%H:%M").replace(tzinfo=timezone.utc)

    # Check if the current time is within the peak time ranges
    if peak_start_1 <= utc_time < peak_end_1:
        return "peakstart"
    elif non_peak_start <= utc_time < non_peak_end:
        return "nonpeak"
    elif peak_start_2 <= utc_time < peak_end_2:
        return "peakend"
    else:
        return "nonmkt"

print(peak_time())

