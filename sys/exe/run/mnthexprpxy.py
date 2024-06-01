from datetime import datetime

def format_expiry_date(date_str):
    # Parse the input date string
    date = datetime.strptime(date_str, "%Y-%m-%d")

    # Format the month as abbreviated name (e.g., APR, MAY, JUN)
    month_abbr = date.strftime("%b").upper()

    # Format the year as 2-digit number
    year_2digit = date.strftime("%y")

    return year_2digit, month_abbr
