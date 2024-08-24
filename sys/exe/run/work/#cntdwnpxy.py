from datetime import datetime, timedelta, timezone

def nonpeak_countdown():
    # Define the start and end times for the countdown in UTC
    start_time_utc = datetime.strptime("03:53", "%H:%M").time()
    end_time_utc = datetime.strptime("09:52", "%H:%M").time()

    # Get the current UTC time
    current_time_utc = datetime.now(timezone.utc).time()

    # Calculate the total duration of the non-peak period
    total_duration = timedelta(hours=end_time_utc.hour, minutes=end_time_utc.minute) - timedelta(hours=start_time_utc.hour, minutes=start_time_utc.minute)

    # Calculate the remaining time within the non-peak period
    remaining_time = timedelta(hours=end_time_utc.hour, minutes=end_time_utc.minute) - timedelta(hours=current_time_utc.hour, minutes=current_time_utc.minute)

    # Calculate the percentage of time passed
    time_passed_percentage = (total_duration - remaining_time) / total_duration

    # Calculate the countdown value
    countdown_value = round(10 * (1 - time_passed_percentage), 1)

    return countdown_value

# Test the function
countdown = nonpeak_countdown()
print("Countdown value:", countdown)
