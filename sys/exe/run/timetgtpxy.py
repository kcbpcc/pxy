from datetime import datetime, timedelta, timezone

def timetgt():
    # Define the start and end values for timetgt
    start_timetgt = 21
    end_timetgt = 11

    # Define the start and end times for the countdown in UTC
    start_time_utc = datetime.strptime("3:45", "%H:%M").time()
    end_time_utc = datetime.strptime("09:54", "%H:%M").time()

    # Get the current UTC time
    current_time_utc = datetime.now(timezone.utc).time()

    # Calculate the total duration of the non-peak period
    total_duration = (end_time_utc.hour - start_time_utc.hour) * 60 + (end_time_utc.minute - start_time_utc.minute)

    # Calculate the elapsed time within the non-peak period
    elapsed_time = (current_time_utc.hour - start_time_utc.hour) * 60 + (current_time_utc.minute - start_time_utc.minute)

    # Calculate the percentage of time passed
    time_passed_percentage = elapsed_time / total_duration

    # Calculate the timetgt value
    timetgt = start_timetgt - (start_timetgt - end_timetgt) * time_passed_percentage

    # Ensure timetgt never goes below 10
    timetgt = max(timetgt, 10)

    return round(timetgt, 1)

#print(timetgt())
