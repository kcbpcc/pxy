import pandas as pd
from datetime import datetime

def cdslcheck(combined_df):
    cdsl_df = combined_df.copy()

    # Convert 'authorised_date' column to datetime format
    cdsl_df['authorised_date'] = pd.to_datetime(cdsl_df['authorised_date'])

    # Combine date and quantity in the format 'YYYY-MM-DD HH:MM:SS': qty
    cdsl_df['cdsl_info'] = cdsl_df.apply(lambda row: f"{row['authorised_date']}: {row['authorised_quantity']}", axis=1)

    # Get today's date and convert it to datetime object
    today = datetime.now().date()
    today_datetime = datetime.combine(today, datetime.min.time())

    # Filter the DataFrame based on the conditions: authorised_date is not today's date
    check_cdsl_df = cdsl_df[(cdsl_df['authorised_date'].dt.date != today_datetime)]

    # Return the filtered DataFrame
    return check_cdsl_df

