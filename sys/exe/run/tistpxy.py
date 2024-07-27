from datetime import datetime
import pytz
from trndpxy import  get_action
nHA_ACTION, nHA_POWER, nDay_Change, nOpen_Change = get_action(^NSEI')
from clorpxy import BRIGHT_YELLOW, BRIGHT_RED, BRIGHT_GREEN, RESET
def print_current_datetime_in_ist():
    utc_now = datetime.utcnow()
    utc_timezone = pytz.timezone('UTC')
    utc_now = utc_timezone.localize(utc_now)
    ist_timezone = pytz.timezone('Asia/Kolkata')
    ist_now = utc_now.astimezone(ist_timezone)
    formatted_datetime = (
        f"|🌏{ist_now.strftime('%d')} "  # Bright yellow color and underline
        f"{ist_now.strftime('%B'):9} {ist_now.strftime('%Y')}|"  # Month, year
        f"🕛{ist_now.strftime('%A'):9}|"  # Day
        f"⏰{ist_now.strftime('%I:%M%p')}"  # Time (reset color)
    )
    if nDay_Change > 0:
        print(f"{BRIGHT_GREEN}{formatted_datetime}{RESET}")
    elif nDay_Change < 0:
        print(f"{BRIGHT_RED}{formatted_datetime}{RESET}")
    else:
        print(f"{BRIGHT_YELLOW}{formatted_datetime}{RESET}")
print_current_datetime_in_ist()


