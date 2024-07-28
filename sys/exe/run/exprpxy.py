from datetime import datetime

def month_expiry_date():
    # Get the current date
    current_date = datetime.now()

    # Determine the next month
    current_month = current_date.month
    next_month = current_month % 12 + 1
    # Determine the year, incrementing if next month is January
    year = current_date.year + (current_month // 12)

    # Format the month as abbreviated name (e.g., APR, MAY, JUN)
    expiry_month = datetime(year, next_month, 1).strftime("%b").upper()

    # Format the year as 2-digit number
    expiry_year = datetime(year, next_month, 1).strftime("%y")
    
    # Set expiry_day to None
    expiry_day = None

    return expiry_year, expiry_month, expiry_day

# Example usage:
#expiry_year, expiry_month, expiry_day = month_expiry_date()
#print(expiry_year, expiry_month, expiry_day)

