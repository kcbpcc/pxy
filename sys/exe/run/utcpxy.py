from datetime import datetime, timezone

def peak_time():
    # Get the current UTC time without date component
    current_utc_time = datetime.utcnow().time()

    # Define the peak time ranges
    peak_time_0_start = datetime.strptime("00:00", "%H:%M").time()
    peak_time_0_end = datetime.strptime("03:00", "%H:%M").time()
    #print("Peak Time 0 Range:", peak_time_0_start, "-", peak_time_0_end)

    peak_time_1a_start = datetime.strptime("03:01", "%H:%M").time()
    peak_time_1a_end = datetime.strptime("03:44", "%H:%M").time()
    #print("Peak Time 1 Range:", peak_time_1_start, "-", peak_time_1_end)

    peak_time_1_start = datetime.strptime("03:44", "%H:%M").time()
    peak_time_1_end = datetime.strptime("03:47", "%H:%M").time()
    #print("Peak Time 1 Range:", peak_time_1_start, "-", peak_time_1_end)

    peak_time_2_start = datetime.strptime("03:47", "%H:%M").time()
    peak_time_2_end = datetime.strptime("09:51", "%H:%M").time()
    #print("Peak Time 2 Range:", peak_time_2_start, "-", peak_time_2_end)

    peak_time_3_start = datetime.strptime("09:51", "%H:%M").time()
    peak_time_3_end = datetime.strptime("10:01", "%H:%M").time()
    #print("Peak Time 3 Range:", peak_time_3_start, "-", peak_time_3_end)

    peak_time_3a_start = datetime.strptime("10:01", "%H:%M").time()
    peak_time_3a_end = datetime.strptime("10:03", "%H:%M").time()
    #print("Peak Time 3 Range:", peak_time_3_start, "-", peak_time_3_end)

    peak_time_4_start = datetime.strptime("10:03", "%H:%M").time()
    peak_time_4_end = datetime.strptime("23:59", "%H:%M").time()
    #print("Peak Time 4 Range:", peak_time_4_start, "-", peak_time_4_end)

    # Check current time against defined ranges
    if peak_time_0_start <= current_utc_time <= peak_time_0_end:
        return "NONMKT"
    elif peak_time_1a_start <= current_utc_time <= peak_time_1a_end:
        return "PREPEAK"    
    elif peak_time_1_start <= current_utc_time <= peak_time_1_end:
        return "PEAKSTART"
    elif peak_time_2_start <= current_utc_time <= peak_time_2_end:
        return "NONPEAK"
    elif peak_time_3_start <= current_utc_time <= peak_time_3_end:
        return "PEAKEND"
    elif peak_time_3a_start <= current_utc_time <= peak_time_3a_end:
        return "MKTEND"
    elif peak_time_4_start <= current_utc_time <= peak_time_4_end:
        return "NONMKT"

    # If none of the above conditions are met, return a default value
    return "UNKNOWN"

