from datetime import datetime, timezone

def peak_time():
    # Get the current UTC time
    utc_time = datetime.utcnow().replace(tzinfo=timezone.utc)

    # Define the peak time ranges
    peak_time_1_start = datetime.strptime("03:45", "%H:%M").replace(tzinfo=timezone.utc)
    peak_time_1_end = datetime.strptime("04:00", "%H:%M").replace(tzinfo=timezone.utc)
    
    peak_time_2_start = datetime.strptime("09:52", "%H:%M").replace(tzinfo=timezone.utc)
    peak_time_2_end = datetime.strptime("10:00", "%H:%M").replace(tzinfo=timezone.utc)

    peak_time_3_start = datetime.strptime("04:01", "%H:%M").replace(tzinfo=timezone.utc)
    peak_time_3_end = datetime.strptime("09:51", "%H:%M").replace(tzinfo=timezone.utc)

    # Check if the current time is within the peak time ranges
    in_peak_time_1 = peak_time_1_start <= utc_time <= peak_time_1_end
    in_peak_time_2 = peak_time_2_start <= utc_time <= peak_time_2_end
    in_peak_time_3 = peak_time_3_start <= utc_time <= peak_time_3_end

    if in_peak_time_1:
        return "peakstart"
    elif in_peak_time_2:
        return "peakend"
    elif in_peak_time_3:
        return "nonpeak"
    else:
        return "nonmkt"

