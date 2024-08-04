from datetime import datetime, timedelta

def calculate_cycle(current_time):
    # Define time intervals in UTC with clear boundaries
    MKTSTART_start_S = datetime.strptime("03:30", "%H:%M").time()
    MKTSTART_start_E = datetime.strptime("04:00:59.999999", "%H:%M:%S.%f").time()

    MKTRUN_start_S = datetime.strptime("04:01", "%H:%M").time()
    MKTRUN_start_E = datetime.strptime("09:29:59.999999", "%H:%M:%S.%f").time()

    MKTEND_start_S = datetime.strptime("09:30", "%H:%M").time()
    MKTEND_start_E = datetime.strptime("09:59:59.999999", "%H:%M:%S.%f").time()

    MKTNONE_start_S1 = datetime.strptime("10:00", "%H:%M").time()
    MKTNONE_start_E1 = datetime.strptime("23:59:59.999999", "%H:%M:%S.%f").time()

    MKTNONE_start_S2 = datetime.strptime("00:00", "%H:%M").time()
    MKTNONE_start_E2 = datetime.strptime("03:29:59.999999", "%H:%M:%S.%f").time()

    # Convert current time to datetime object with today's date
    current_datetime = datetime.combine(datetime.today(), current_time)

    # Check if the current time is within the MKTSTART interval
    if MKTSTART_start_S <= current_time <= MKTSTART_start_E:
        return 1  # 1 second for MKTSTART

    # Check if the current time is within the MKTRUN interval
    elif MKTRUN_start_S <= current_time <= MKTRUN_start_E:
        return 6  # 5 seconds for MKTRUN

    # Check if the current time is within the MKTEND interval
    elif MKTEND_start_S <= current_time <= MKTEND_start_E:
        return 1  # 1 second for MKTEND

    # Check if the current time is within the MKTNONE intervals
    elif (MKTNONE_start_S1 <= current_time <= MKTNONE_start_E1) or (MKTNONE_start_S2 <= current_time <= MKTNONE_start_E2):
        # Calculate the time remaining until the next interval
        if current_time <= MKTNONE_start_E1:
            next_interval_start = datetime.combine(datetime.today(), MKTNONE_start_S2)
        else:
            next_interval_start = datetime.combine(datetime.today() + timedelta(days=1), MKTNONE_start_S2)
        
        remaining_time = (next_interval_start - current_datetime) if current_datetime <= next_interval_start else (timedelta(days=1) + next_interval_start - current_datetime)
        remaining_time /= 4  # Divide by 4
        return round(remaining_time.total_seconds())

    else:
        return 6  # Default value for times outside defined intervals

# Get the current UTC time
current_utc_time = datetime.utcnow().time()

# Calculate loop duration based on current time
cycle = calculate_cycle(current_utc_time)
#print(f"Current cycle time: {cycle} seconds")

# Calculate loop duration based on current time
#cycle = calculate_cycle(current_utc_time)
#print(f"Current cycle time: {cycle} seconds")

# Calculate loop duration based on current time
#cycle = calculate_cycle(current_utc_time)
#print(f"Current cycle time: {cycle} seconds")

