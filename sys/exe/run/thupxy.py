from datetime import datetime, timedelta

def get_this_thursday(adjust=7):
    current_date = datetime.now()
    days_until_this_thursday = (3 - current_date.weekday() + 7) % 7
    if days_until_this_thursday == 0:
        this_thursday = current_date
    else:
        this_thursday = current_date + timedelta(days=days_until_this_thursday)

    # Calculate the last day of the month
    next_month = this_thursday.replace(day=28) + timedelta(days=4)  # ensures getting to the next month
    last_day_of_month = next_month - timedelta(days=next_month.day)

    # Check if this Thursday falls in the last week of the month
    if (last_day_of_month - this_thursday).days < 7:
        expiry_year = this_thursday.strftime("%y")
        expiry_month = this_thursday.strftime("%b").upper()  # Convert month to all caps
        return expiry_year, expiry_month, ''

    # Adjust the date
    adjusted_date = this_thursday + timedelta(days=adjust)

    # Formatting
    expiry_year = adjusted_date.strftime("%y")
    expiry_month = adjusted_date.strftime("%b").upper()  # Convert month to all caps
    expiry_day = adjusted_date.strftime("%d").zfill(2)

    return expiry_year, expiry_month, expiry_day
