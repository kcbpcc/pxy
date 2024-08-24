from datetime import datetime, timedelta

def get_this_thursday(adjest=7):
    current_date = datetime.now()
    days_until_this_thursday = (3 - current_date.weekday() + 7) % 7
    if days_until_this_thursday == 0:
        # If today is Thursday, move to the next Thursday
        days_until_this_thursday = 7
    this_thursday = current_date + timedelta(days=days_until_this_thursday)
    last_day_of_month = (this_thursday.replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)
    if this_thursday.month != (this_thursday + timedelta(days=7)).month:
        if this_thursday.day > last_day_of_month.day - 7:
            expiry_year = this_thursday.strftime("%y")
            expiry_month = this_thursday.strftime("%b").upper()  # Convert to all caps
            expiry_day = ''  # Empty day
            return expiry_year, expiry_month, expiry_day
    expiry_year = this_thursday.strftime("%y")
    expiry_month = this_thursday.strftime("%b").upper()  # Convert to all caps
    expiry_day_adjust = timedelta(days=adjest)  # Adjustment of days
    expiry_day = (this_thursday - expiry_day_adjust).strftime("%d").zfill(2)
    return expiry_year, expiry_month, expiry_day

