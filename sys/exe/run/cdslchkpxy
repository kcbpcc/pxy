import pandas as pd
from datetime import datetime

def check(combined_df):
    # Create a copy of the DataFrame to avoid modifying the original DataFrame
    cdsl_df = combined_df.copy()

    # Extract date and quantity from the 'authorisation' column
    cdsl_df['cdsldate'] = cdsl_df['authorisation'].str.extract(r"(\d{4}-\d{2}-\d{2})")
    cdsl_df['cdslqty'] = cdsl_df['authorisation'].str.extract(r"(\d+)}}$").astype(int)

    # Convert the extracted date to datetime object
    cdsl_df['cdsldate'] = pd.to_datetime(cdsl_df['cdsldate'])

    # Get today's date
    today = datetime.now().date()

    # Filter the DataFrame based on the condition and include the 'qty' and 'tradingsymbol' columns
    filtered_cdsl_df = cdsl_df[cdsl_df['cdsldate'].dt.date != today]

    # Return the filtered DataFrame
    return filtered_cdsl_df
