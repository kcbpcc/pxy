from datetime import datetime, timezone

def peak_time():
    # Get the current UTC time
    utc_time = datetime.utcnow().replace(tzinfo=timezone.utc)

    # Define the peak time ranges
    peak_time_0_start = datetime.strptime("00:00", "%H:%M").replace(tzinfo=timezone.utc)
    peak_time_0_end = datetime.strptime("03:44", "%H:%M").replace(tzinfo=timezone.utc)

    peak_time_1_start = datetime.strptime("03:45", "%H:%M").replace(tzinfo=timezone.utc)
    peak_time_1_end = datetime.strptime("03:59", "%H:%M").replace(tzinfo=timezone.utc)

    peak_time_2_start = datetime.strptime("04:00", "%H:%M").replace(tzinfo=timezone.utc)
    peak_time_2_end = datetime.strptime("09:50", "%H:%M").replace(tzinfo=timezone.utc)

    peak_time_3_start = datetime.strptime("09:51", "%H:%M").replace(tzinfo=timezone.utc)
    peak_time_3_end = datetime.strptime("17:00", "%H:%M").replace(tzinfo=timezone.utc)

    peak_time_4_start = datetime.strptime("17:01", "%H:%M").replace(tzinfo=timezone.utc)
    peak_time_4_end = datetime.strptime("23:59", "%H:%M").replace(tzinfo=timezone.utc)

    # Check current time against defined ranges
    if peak_time_0_start <= utc_time <= peak_time_0_end:
        return "NONMKT"
    elif peak_time_1_start <= utc_time <= peak_time_1_end:
        return "PEAKSTART"
    elif peak_time_2_start <= utc_time <= peak_time_2_end:
        return "NONPEAK"
    elif peak_time_3_start <= utc_time <= peak_time_3_end:
        return "PEAKEND"
    elif peak_time_4_start <= utc_time <= peak_time_4_end:
        return "NONMKT"

    # If none of the above conditions are met, return a default value
    return "UNKNOWN"

# Test the function
print(peak_time())


  
