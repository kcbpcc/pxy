import sys
import traceback
import pandas as pd
from login_get_kite import get_kite, remove_token
from cnstpxy import dir_path
from toolkit.logger import Logger

# Define logging
logging = Logger(30, dir_path + "main.log")

def get_holdings_info(resp_list, broker):
    try:
        df = pd.DataFrame(resp_list)
        df['source'] = 'holdings'
        return df
    except Exception as e:
        logging.error(f"Error occurred in get_holdings_info: {e}")
        return None

def get_positions_info(resp_list, broker):
    try:
        df = pd.DataFrame(resp_list)
        df['source'] = 'positions'
        return df
    except Exception as e:
        logging.error(f"Error occurred in get_positions_info: {e}")
        return None

def process_data():
    # Redirect stdout to output.txt
    sys.stdout = open('output.txt', 'w')

    # Attempt to get broker instance
    broker = None
    try:
        broker = get_kite()
    except Exception as e:
        remove_token(dir_path)
        logging.error(f"Error in getting kite instance: {e}")
        print(traceback.format_exc())
        sys.exit(1)
    finally:
        # Ensure to close the file and restore stdout
        if sys.stdout != sys.__stdout__:
            sys.stdout.close()
            sys.stdout = sys.__stdout__

    try:
        # If broker is obtained successfully, proceed with data processing
        holdings_response = broker.kite.holdings()
        positions_response = broker.kite.positions()['net']
        
        holdings_df = get_holdings_info(holdings_response, broker)
        positions_df = get_positions_info(positions_response, broker)

        # Check if 'tradingsymbol' is present in both dataframes
        if 'tradingsymbol' not in holdings_df.columns or 'tradingsymbol' not in positions_df.columns:
            raise KeyError("'tradingsymbol' column not found in holdings_df or positions_df")

        # Merge holdings_df and positions_df on 'tradingsymbol'
        merged_df = pd.merge(holdings_df, positions_df, on='tradingsymbol', how='outer')

        # Filter merged_df to include only rows where product_x == 'CNC' and used_quantity > 0
        merged_df_filtered = merged_df[(merged_df['product_x'] == 'CNC') & (merged_df['used_quantity'] > 0)].copy()

        # Calculate PL% and PnL
        merged_df_filtered['SN'] = range(1, len(merged_df_filtered) + 1)  # Serial number starting from 1
        merged_df_filtered['STOCK'] = merged_df_filtered['tradingsymbol']
        merged_df_filtered['QTY'] = merged_df_filtered['used_quantity'].astype(int)
        merged_df_filtered['PL%'] = ((merged_df_filtered['average_price_y'] - merged_df_filtered['average_price_x']) / merged_df_filtered['average_price_y']) * 100
        merged_df_filtered['PL%'] = merged_df_filtered['PL%'].round(2)
        merged_df_filtered['PnL'] = merged_df_filtered.apply(lambda row: row['used_quantity'] * (row['average_price_y'] - row['average_price_x']), axis=1).astype(int)
        
        # Select specific columns from filtered merged_df and reorder
        merged_df_filtered = merged_df_filtered[['SN', 'STOCK', 'QTY', 'PL%', 'PnL']]

        # Set column widths for printing
        col_widths = [3, 12, 8, 7, 8]

        # Convert DataFrame to formatted string with aligned headers and values
        formatted_str = merged_df_filtered.to_string(index=False, col_space=col_widths)

        # ANSI escape sequence for bright yellow color
        bright_yellow = '\033[93m'
        reset_color = '\033[0m'

        # Print headers with bright yellow color
        headers_str = formatted_str.split('\n', 1)[0]  # Extract headers
        print(f"{bright_yellow}{headers_str}{reset_color}")

        # Print the rest of the formatted string (values)
        print(formatted_str[len(headers_str):])

        # Print "Stocks Booked Profit" right-aligned with 42 spaces
        total_profit = merged_df_filtered['PnL'].sum()
        print(f"\033[92m{total_profit:>42}\033[0m")



        return merged_df_filtered

    except Exception as e:
        logging.error(f"Error occurred in process_data: {e}")
        print(f"An error occurred: {e}")
        traceback.print_exc()
        return None

def main():
    try:
        process_data()
    except Exception as e:
        logging.error(f"Error occurred in main: {e}")
        print(f"An error occurred in main: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    main()

