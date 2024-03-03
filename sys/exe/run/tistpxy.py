from datetime import datetime
import pytz

def print_current_datetime_in_ist():
    # Get the current time in UTC
    utc_now = datetime.utcnow()

    # Set the UTC timezone
    utc_timezone = pytz.timezone('UTC')
    utc_now = utc_timezone.localize(utc_now)

    # Convert to IST (Indian Standard Time)
    ist_timezone = pytz.timezone('Asia/Kolkata')
    ist_now = utc_now.astimezone(ist_timezone)

    formatted_datetime = (
        f"\033[97m\033[4m🗓️ {ist_now.strftime('%d')} "  # Different calendar emoji and underline
        f"{ist_now.strftime('%B'):9} {ist_now.strftime('%Y')}|"  # Month, year
        f"🕛 {ist_now.strftime('%A'):9}|"  # Day
        f"⏰{ist_now.strftime('%I:%M%p')}\033[0m"  # Time (reset color)
    )
    
    # Print the formatted date and time
    print(formatted_datetime)
    
    # Time with white color
    formatted_time = f"\033[97m⏰ {ist_now.strftime('%I:%M%p')}\033[0m"  # Time (reset color)
    return formatted_time

if __name__ == "__main__":
    print_current_datetime_in_ist()
