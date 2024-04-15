import pandas as pd
from datetime import datetime

def cdslcheck(combined_df):
    cdsl_df = combined_df.copy()

    # Extract date and quantity from the 'authorisation' column
    date_qty_extract = cdsl_df['authorisation'].str.extract(r"'pre': {'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})': (\d+)}")

    # Combine date and quantity in the format 'YYYY-MM-DD HH:MM:SS': qty
    cdsl_df['cdsl_info'] = date_qty_extract.apply(lambda x: f"{x[0]}: {x[1]}", axis=1)

    # Convert the extracted date to datetime format
    cdsl_df['cdsldate'] = pd.to_datetime(date_qty_extract[0], format='%Y-%m-%d %H:%M:%S', errors='coerce')

    # Get today's date and convert it to datetime object
    today = datetime.now().date()
    today_datetime = datetime.combine(today, datetime.min.time())

    # Filter the DataFrame based on the conditions: cdsldate is not today's date and cdslqty is not equal to qty
    check_cdsl_df = cdsl_df[(cdsl_df['cdsldate'].dt.date != today_datetime.date())]

    # Return the filtered DataFrame
    return check_cdsl_df
