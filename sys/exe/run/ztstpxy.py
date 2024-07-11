import sys
import traceback
import pandas as pd
from tabulate import tabulate
from login_get_kite import get_kite, remove_token
from cnstpxy import dir_path
from toolkit.logger import Logger

# Define logging
logging = Logger(30, dir_path + "main.log")

def get_holdingsinfo(resp_list, broker):
    try:
        df = pd.DataFrame(resp_list)
        df['source'] = 'holdings'
        return df
    except Exception as e:
        print(f"An error occurred in holdings: {e}")
        return None

def get_positionsinfo(resp_list, broker):
    try:
        df = pd.DataFrame(resp_list)
        df['source'] = 'positions'
        return df
    except Exception as e:
        print(f"An error occurred in positions: {e}")
        return None

def process_data():
    try:
        broker = get_kite()
        holdings_response = broker.kite.holdings()
        positions_response = broker.kite.positions()['net']
        
        holdings_df = get_holdingsinfo(holdings_response, broker)
        positions_df = get_positionsinfo(positions_response, broker)

        # Ensure both dataframes have the necessary columns
        if 'tradingsymbol' not in holdings_df.columns or 'tradingsymbol' not in positions_df.columns:
            raise KeyError("'tradingsymbol' column not found in holdings_df or positions_df")

        # Merge holdings_df and positions_df on 'tradingsymbol'
        merged_df = pd.merge(holdings_df, positions_df, on='tradingsymbol', how='outer')

        # Filter merged_df to include only rows where product_x == 'CNC' and used_quantity > 0
        merged_df_filtered = merged_df[(merged_df['product_x'] == 'CNC') & (merged_df['used_quantity'] > 0)]
        
        # Select specific columns from filtered merged_df
        merged_df_filtered = merged_df_filtered[['tradingsymbol', 'average_price_x', 'average_price_y']]
        
        # Calculate profit percentage for each row
        merged_df_filtered['PL%'] = ((merged_df_filtered['average_price_y'] - merged_df_filtered['average_price_x']) / merged_df_filtered['average_price_x']) * 100
        merged_df_filtered['PL%'] = merged_df_filtered['PL%'].astype(float)

        print(f"Total Profit Percentage: {merged_df_filtered['PL%'].sum()}")

        return merged_df_filtered

    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()
        return None



def save_to_csv(df, filename):
    try:
        # Rename columns as per specified format
        df.rename(columns={
            'tradingsymbol': 'Stock',
            'average_price_x': 'Buy',
            'average_price_y': 'PL%'
        }, inplace=True)

        # Convert numeric columns to integers
        df['Buy'] = df['Buy'].astype(int)
        df['PL%'] = df['PL%'].astype(int)

        # Remove index and save to CSV
        df.to_csv(filename, index=False)
        print(f"Dataframe saved to {filename}")

    except Exception as e:
        print(f"Error saving dataframe to CSV: {e}")
        traceback.print_exc()

def main():
    try:
        result_df = process_data()
        
        if result_df is not None:
            # Adjust stock codes to max 5 characters
            result_df['tradingsymbol'] = result_df['tradingsymbol'].apply(lambda x: x[:5])

            # Convert dataframe to list of lists for tabulate
            data = result_df.values.tolist()
            headers = ["Stock", "Buy", "PL%"]

            # Print the result as a formatted table with integers only, without row lines
            print(tabulate(data, headers=headers, tablefmt="fancy_grid", numalign="right", stralign="right", floatfmt=".0f", showindex=False))

            # Save the result to a CSV file
            save_to_csv(result_df, 'output.csv')

    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    main()
