import pandas as pd
from datetime import datetime

def cdslcheck(combined_df):
    # Create a copy of the DataFrame to avoid modifying the original DataFrame
    cdsl_df = combined_df.copy()

    # Extract date and quantity from the 'authorisation' column
    cdsl_df['cdsldate'] = cdsl_df['authorisation'].str.extract(r"(\d{4}-\d{2}-\d{2})")
    cdsl_df['cdslqty'] = cdsl_df['authorisation'].str.extract(r"(\d+)}}$").astype(int)

    # Convert the extracted date to datetime object
    cdsl_df['cdsldate'] = pd.to_datetime(cdsl_df['cdsldate'])

    # Get today's date and convert it to datetime object
    today = datetime.now().date()
    today_datetime = datetime.combine(today, datetime.min.time())

    # Filter the DataFrame based on the conditions: cdsldate is not today's date and cdslqty is not equal to qty
    filtered_cdsl_df = cdsl_df[(cdsl_df['cdsldate'] != today_datetime) & (cdsl_df['cdslqty'] != cdsl_df['qty'])]

    # Return the filtered DataFrame
    return filtered_cdsl_df

combined_df = pd.DataFrame(data)

# Call the check function with combined_df as argument
filtered_cdsl_df = check(combined_df)

# Display the filtered DataFrame with cdsldate, cdslqty, qty, and tradingsymbol columns
print(filtered_cdsl_df[['cdsldate', 'cdslqty', 'qty', 'tradingsymbol']])

