from datetime import datetime
import pytz

# Constants from nftpxy and clorpxy modules
from nftpxy import nse_action, nse_power, Day_Change, Open_Change, OPTIONS  
from clorpxy import SILVER, UNDERLINE, RED, GREEN, YELLOW, RESET, BRIGHT_YELLOW, BRIGHT_RED, BRIGHT_GREEN, BOLD, GREY

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
        f"🗓️ {ist_now.strftime('%d')} "  # Bright yellow color and underline
        f"{ist_now.strftime('%B'):9} {ist_now.strftime('%Y')}|"  # Month, year
        f"🕛 {ist_now.strftime('%A'):9}|"  # Day
        f"⏰{ist_now.strftime('%I:%M%p')}"  # Time (reset color)
    )
    if Day_Change > 0:
        print(f"{BRIGHT_GREEN}{formatted_datetime}{Day_Change}{RESET}")
    elif Day_Change < 0:
        print(f"{BRIGHT_RED}{formatted_datetime}{Day_Change}{RESET}")
    else:
        print(f"{BRIGHT_YELLOW}{formatted_datetime}{Day_Change}{RESET}")

