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

    # Format the date and time with emojis
    formatted_datetime = (
        f"\033[95m🗓️ {ist_now.strftime('%d')} "  # Different calendar emoji
        f"{ist_now.strftime('%B')} {ist_now.strftime('%Y')} |"  # Month, year
        f"🕛 {ist_now.strftime('%A')} |"   # Day
        f"⏰ {ist_now.strftime('%I:%M%p')}\033[0m"  # Time (reset color)
    )

    # Print the formatted date and time
    print(formatted_datetime)

if __name__ == "__main__":
    print_current_datetime_in_ist()
