import pandas as pd
from datetime import datetime

def cdslcheck(combined_df):
    # Create a copy of the DataFrame to avoid modifying the original DataFrame
    cdsl_df = combined_df.copy()

    # Extract date and quantity from the 'authorisation' column
    date_qty_extract = cdsl_df['authorisation'].str.extract(r"\{'pre': \{'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})': (\d+)\}}")
    
    # Extract date and quantity into separate columns
    cdsl_df['cdsldate'] = pd.to_datetime(date_qty_extract[0])
    
    # Fill NaN values in quantity column with 0 and then convert to integers
    cdsl_df['cdslqty'] = date_qty_extract[1].fillna(0).astype(int)

    # Get today's date and convert it to datetime object
    today = datetime.now().date()
    today_datetime = datetime.combine(today, datetime.min.time())

    # Filter the DataFrame based on the conditions: cdsldate is not today's date and cdslqty is not equal to qty
    check_cdsl_df = cdsl_df[(cdsl_df['cdsldate'] != today_datetime) & (cdsl_df['cdslqty'] != cdsl_df['qty'])]

    # Return the filtered DataFrame
    return check_cdsl_df
