import sys
import traceback
import pandas as pd
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
        # Redirect stdout to output.txt
        sys.stdout = open('output.txt', 'w')

        # Attempt to get broker instance
        broker = None
        try:
            broker = get_kite()
        except Exception as e:
            remove_token(dir_path)
            print(traceback.format_exc())
            logging.error(f"{str(e)} unable to get holdings")
            sys.exit(1)

        # If broker is obtained successfully, proceed with data processing
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

        # Use .loc to set values without warning
        merged_df_filtered.loc[:, 'STOCK'] = merged_df_filtered['tradingsymbol']
        merged_df_filtered.loc[:, 'QTY'] = merged_df_filtered['used_quantity']
        merged_df_filtered.loc[:, 'PL%'] = ((merged_df_filtered['average_price_y'] - merged_df_filtered['average_price_x']) / merged_df_filtered['average_price_y']) * 100
        merged_df_filtered.loc[:, 'PnL'] = merged_df_filtered.apply(lambda row: row['used_quantity'] * (row['average_price_y'] - row['average_price_x']), axis=1)
        
        # Select specific columns from filtered merged_df
        merged_df_filtered = merged_df_filtered[['STOCK', 'QTY', 'PL%', 'PnL']]

        # Print filtered dataframe
        print(merged_df_filtered)

        # Calculate total profit
        total_profit = merged_df_filtered['PnL'].sum()
        
        print(f"Total Profit: {total_profit}")

        return merged_df_filtered

    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()
        return None

    finally:
        # Ensure to close the file and restore stdout
        if sys.stdout != sys.__stdout__:
            sys.stdout.close()
            sys.stdout = sys.__stdout__

def main():
    try:
        process_data()
    except Exception as e:
        print(f"An error occurred in main: {e}")
        logging.error(f"An error occurred in main: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    main()
