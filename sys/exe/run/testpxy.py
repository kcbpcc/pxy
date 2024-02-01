from nftpxy import OPTIONS
import datetime

def get_current_thursday():
    today = datetime.datetime.now()
    
    # Calculate days until current Thursday (considering 0 as Sunday)
    days_until_thursday = (3 - int(today.strftime("%w"))) % 7
    current_thursday = today - datetime.timedelta(days=days_until_thursday)
    
    return current_thursday

def format_options_string(options_str):
    current_thursday = get_current_thursday()
    
    # Extract components from the given string
    year = current_thursday.strftime("%y")
    month = current_thursday.strftime("%m")
    thursday_date = current_thursday.strftime("%d")
    
    # Replace placeholders in the string
    formatted_str = options_str.replace("{Year}", year).replace("{Month}", month).replace("{THURSDAY_DATE}", thursday_date).replace("{OPTIONS}", str(OPTIONS))
    
    return formatted_str

# Example usage
options_str = "NIFTY{Year}{Month}{THURSDAY_DATE}{OPTIONS}PE"
result = format_options_string(options_str)
print(result)

