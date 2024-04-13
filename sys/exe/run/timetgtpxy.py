from datetime import datetime, timedelta, timezone

def timetgt():
    # Define the start and end times for the countdown in UTC
    start_time_utc = datetime.strptime("3:45", "%H:%M").time()
    end_time_utc = datetime.strptime("09:54", "%H:%M").time()

    # Get the current UTC time
    current_time_utc = datetime.now(timezone.utc).time()

    # Calculate the total duration of the non-peak period
    total_duration = (end_time_utc.hour - start_time_utc.hour) * 60 + (end_time_utc.minute - start_time_utc.minute)

    # Calculate the remaining time within the non-peak period
    remaining_time = (end_time_utc.hour - current_time_utc.hour) * 60 + (end_time_utc.minute - current_time_utc.minute)

    # Calculate the percentage of time passed
    time_passed_percentage = (total_duration - remaining_time) / total_duration

    # Calculate the timetgt value
    timetgt = round(10 * (1 - time_passed_percentage), 1)

    # Ensure timetgt never goes below 5
    timetgt = max(timetgt, 5)

    return timetgt

# Test the function
print(timetgt())
