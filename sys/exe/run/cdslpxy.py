import pandas as pd
from datetime import datetime
from cmbddfpxy import process_data

combined_df = process_data()

def cdslcheck(combined_df):
    cdsl_df = combined_df.copy()

    # Convert 'authorised_date' column to datetime format
    cdsl_df['authorised_date'] = pd.to_datetime(cdsl_df['authorised_date'])

    # Combine date and quantity in the format 'YYYY-MM-DD HH:MM:SS': qty
    cdsl_df['cdsl_info'] = cdsl_df.apply(lambda row: f"{row['authorised_date'].date()}: {row['authorised_quantity']}", axis=1)

    # Convert the extracted quantity to integers and create 'cdslqty' column
    cdsl_df['cdslqty'] = cdsl_df['authorised_quantity']

    # Convert the extracted date to datetime format and create 'cdsldate' column
    cdsl_df['cdsldate'] = cdsl_df['authorised_date'].dt.date
    cdsl_df['cdsldate'] = pd.to_datetime(cdsl_df['cdsldate'])

    # Get today's date and convert it to datetime object
    today = datetime.now().date()
    today_datetime = datetime.combine(today, datetime.min.time())

    check_cdsl_df = cdsl_df[((cdsl_df['cdsldate'].dt.date != today_datetime.date()) | 
                             (cdsl_df['qty'] != cdsl_df['cdslqty'])) & 
                            (cdsl_df['source'] == 'holdings')]
    return check_cdsl_df

output_df = cdslcheck(combined_df)
output_df.rename(columns={'tradingsymbol': 'stock'}, inplace=True)
output_df['stock'] = output_df['stock'].str[:7]  # Limiting to a maximum of 7 characters

if output_df.empty:
    print("You are all set to fire")
else:
    print(output_df[['cdsldate', 'cdslqty', 'qty', 'stock']])

