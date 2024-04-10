from datetime import datetime
import pytz
from nftpxy import nse_action, nse_power, Day_Change, Open_Change, OPTIONS  
from clorpxy import SILVER, UNDERLINE, RED, GREEN, YELLOW, RESET, BRIGHT_YELLOW, BRIGHT_RED, BRIGHT_GREEN, BOLD, GREY
def print_current_datetime_in_ist():
    utc_now = datetime.utcnow()
    utc_timezone = pytz.timezone('UTC')
    utc_now = utc_timezone.localize(utc_now)
    ist_timezone = pytz.timezone('Asia/Kolkata')
    ist_now = utc_now.astimezone(ist_timezone)
    formatted_datetime = (
        f"\033[93m\033[4m🗓️ {ist_now.strftime('%d')} "  
        f"{ist_now.strftime('%B'):9} {ist_now.strftime('%Y')}|"  
        f"🕛 {ist_now.strftime('%A'):9}"  
        f"{formatted_time()}\033[0m"  
    )
    print(formatted_datetime)
def formatted_time():
    ist_now = datetime.now(pytz.timezone('Asia/Kolkata'))
    formatted_time = f"\033[97m⏰ {ist_now.strftime('%I:%M%p')}"
    return formatted_time
if __name__ == "__main__":
    print_current_datetime_in_ist()
    if Day_Change > 0:
        print(f"{BRIGHT_GREEN}Day Change: {Day_Change}{RESET}")
    elif Day_Change < 0:
        print(f"{BRIGHT_RED}Day Change: {Day_Change}{RESET}")
    else:
        print(f"{BRIGHT_YELLOW}Day Change: {Day_Change}{RESET}")
