from datetime import datetime, timedelta

def month_expiry_date():
    # Get the current date
    current_date = datetime.now()

    # Add 9 days to the current date
    expiry_date_offset = current_date + timedelta(days=9)

    # Format the month as abbreviated name (e.g., APR, MAY, JUN)
    expiry_month = expiry_date_offset.strftime("%b").upper()

    # Format the year as 2-digit number
    expiry_year = expiry_date_offset.strftime("%y")

    # Format the day
    expiry_day = expiry_date_offset.strftime("%d")

    return expiry_year, expiry_month, expiry_day

