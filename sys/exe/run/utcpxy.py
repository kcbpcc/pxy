from datetime import datetime, timezone

def peak_time():
    # Get the current UTC time
    utc_time = datetime.utcnow().replace(tzinfo=timezone.utc)

    # Define the peak time ranges
    peak_time_1_start = datetime.strptime("03:45", "%H:%M").replace(tzinfo=timezone.utc)
    peak_time_1_end = datetime.strptime("04:00", "%H:%M").replace(tzinfo=timezone.utc)
    
    peak_time_2_start = datetime.strptime("09:45", "%H:%M").replace(tzinfo=timezone.utc)
    peak_time_2_end = datetime.strptime("10:00", "%H:%M").replace(tzinfo=timezone.utc)

    peak_time_3_start = datetime.strptime("04:01", "%H:%M").replace(tzinfo=timezone.utc)
    peak_time_3_end = datetime.strptime("09:44", "%H:%M").replace(tzinfo=timezone.utc)

if peak_time_1_start <= utc_time <= peak_time_1_end:
    print("Within peak time 1")
    return "peakstart"
elif peak_time_2_start <= utc_time <= peak_time_2_end:
    print("Within peak time 2")
    return "peakend"
elif peak_time_3_start <= utc_time <= peak_time_3_end:
    print("Within peak time 3")
    return "nonpeak"
else:
    print("Outside of peak times")
    return "nonmkt"
