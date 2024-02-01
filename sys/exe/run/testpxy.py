from nftpxy import OPTIONS
import datetime

def get_current_thursday():
    today = datetime.datetime.now()

    # Check if today is Thursday
    if today.weekday() == 3:  # 0 is Monday, 1 is Tuesday, ..., 6 is Sunday
        return today

    # Calculate days until the next Thursday (considering 0 as Sunday)
    days_until_thursday = (3 - today.weekday()) % 7
    current_thursday = today + datetime.timedelta(days=days_until_thursday)

    return current_thursday

def format_options_string(options_str, instrument):
    current_thursday = get_current_thursday()

    # Extract components from the given string
    year = current_thursday.strftime("%y")
    month = current_thursday.strftime("%m").lstrip('0')  # Remove leading zero
    thursday_date = current_thursday.strftime("%d")

    # Replace placeholders in the string based on the instrument
    formatted_str = options_str.replace("{Year}", year).replace("{Month}", month).replace("{THURSDAY_DATE}", thursday_date).replace("{OPTIONS}", str(OPTIONS))
    
    # Add the instrument (CE or PE) to the formatted string
    formatted_str += instrument

    return formatted_str

# Example usage
options_str = "NIFTY{Year}{Month}{THURSDAY_DATE}{OPTIONS}"
ce_result = format_options_string(options_str, "CE")
pe_result = format_options_string(options_str, "PE")

print(ce_result)
print(pe_result)
