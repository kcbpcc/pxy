from nftpxy import OPTIONS
import datetime

def get_this_thursday():
    today = datetime.datetime.now()
    
    # Calculate days until next Thursday (considering 0 as Sunday)
    days_until_thursday = (3 - int(today.strftime("%w"))) % 7
    this_thursday = today + datetime.timedelta(days=days_until_thursday)
    
    return this_thursday

def format_options_string(options_str):
    this_thursday = get_this_thursday()
    
    # Extract components from the given string
    constant = options_str[:5]
    year = this_thursday.strftime("%y")
    month = this_thursday.strftime("%-m")  # Remove leading zero
    thursday_date = this_thursday.strftime("%d")
    
    # Replace placeholders in the string
    formatted_str = options_str.replace("{OPTIONS}", constant).replace("24", year).replace("2", month).replace("01", thursday_date)
    
    return formatted_str

# Example usage
options_str = "NIFTY24201{OPTIONS}PE"
result = format_options_string(options_str)
print(result)
