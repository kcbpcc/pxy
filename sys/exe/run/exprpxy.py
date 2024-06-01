from datetime import datetime, timedelta

def month_expiry_date():
    # Get the current date
    current_date = datetime.now()

    # Add 7 days to the current date
    expiry_date_offset = current_date + timedelta(days=7)

    # Format the month as abbreviated name (e.g., APR, MAY, JUN)
    month_abbr = expiry_date_offset.strftime("%b").upper()

    # Format the year as 2-digit number
    year_2digit = expiry_date_offset.strftime("%y")
    
    # Set expiry_day to None
    expiry_day = None

    return year_2digit, month_abbr, expiry_day
