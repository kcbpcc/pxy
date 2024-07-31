import sys
import numpy as np
import pandas as pd
from datetime import datetime
import traceback
from login_get_kite import get_kite, remove_token
from cnstpxy import dir_path
from toolkit.logger import Logger
from clorpxy import SILVER, UNDERLINE, RED, GREEN, YELLOW, RESET, BRIGHT_YELLOW, BRIGHT_RED, BRIGHT_GREEN, BOLD, GREY

logging = Logger(30, dir_path + "main.log")

def get_holdings_info(file_path):
    try:
        df = pd.read_csv(file_path)
        df['source'] = 'holdings'
        return df
    except Exception as e:
        logging.error(f"Error occurred in get_holdings_info: {e}")
        return None

def get_positions_info(file_path):
    try:
        df = pd.read_csv(file_path)
        df['source'] = 'positions'
        return df
    except Exception as e:
        logging.error(f"Error occurred in get_positions_info: {e}")
        return None

def process_data_total_profit():
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
        # Initialize total_profit_fo
        total_profit_fo = 0
        
        # If broker is obtained successfully, proceed with data processing
        holdings_df = get_holdings_info('pxyholdings.csv')
        positions_df = get_positions_info('pxypositions.csv')

        if holdings_df is None or positions_df is None:
            raise ValueError("Failed to load holdings or positions data")

        # Check if 'tradingsymbol' is present in both dataframes
        if 'tradingsymbol' not in holdings_df.columns or 'tradingsymbol' not in positions_df.columns:
            raise KeyError("'tradingsymbol' column not found in holdings_df or positions_df")

        # Merge holdings_df and positions_df on 'tradingsymbol'
        merged_df = pd.merge(holdings_df, positions_df, on='tradingsymbol', how='outer')
        merged_df.to_csv('pxymergedcsv.csv', index=False)

        # Filter merged_df to include only rows where product_x == 'CNC' and used_quantity > 0
        merged_df_filtered = merged_df[(merged_df['product_x'] == 'CNC') & (merged_df['used_quantity'] > 0)].copy()
        merged_df_filtered['PnL'] = merged_df_filtered.apply(
            lambda row: row['used_quantity'] * (row['average_price_y'] - row['average_price_x']),
            axis=1
        ).astype(int)
        total_profit = merged_df_filtered['PnL'].sum() if not merged_df_filtered.empty else 0
        
        if not merged_df_filtered.empty:
            # Calculate PL% and PnL
            merged_df_filtered['STOCK'] = merged_df_filtered['tradingsymbol']
            merged_df_filtered['QTY'] = merged_df_filtered['used_quantity'].astype(int)
            merged_df_filtered['PL%'] = ((merged_df_filtered['average_price_y'] - merged_df_filtered['average_price_x']) / merged_df_filtered['average_price_y']) * 100
            merged_df_filtered['PL%'] = merged_df_filtered['PL%'].round(2)
            
            # Select specific columns from filtered merged_df and reorder
            merged_df_filtered = merged_df_filtered[['STOCK', 'QTY', 'PL%', 'PnL']]
            merged_df_filtered.to_csv('pxycncprofit.csv', index=False)
            
            formatted_str = merged_df_filtered.to_string(index=False, header=False)
            # Uncomment and adjust print formatting if needed
            # for line in formatted_str.split('\n'):
            #     print(f"{line:>41}")
        else:
            empty_df = pd.DataFrame(columns=['STOCK', 'QTY', 'PL%', 'PnL'])
            empty_df.to_csv('pxycncprofit.csv', index=False)
            #print("I did not exit any CNC positions today🤔🤔")

        # Processing NFO data
        mergedfo_df = get_positions_info('pxycombined.csv')

        if mergedfo_df is None:
            raise ValueError("Failed to load NFO data")

        mergedfo_df_filtered = mergedfo_df[(mergedfo_df['exchange'] == 'NFO') & (mergedfo_df['day_sell_quantity'] > 0)].copy()
        nfo_df = mergedfo_df_filtered 
        
        # Calculate total profit for NFO positions
        if not mergedfo_df_filtered.empty:
            # Convert 'PnL' column to integer type
            mergedfo_df_filtered['PnL'] = mergedfo_df_filtered['PnL'].astype(int)
            
            # Define the conditions
            condition_qty_gt_0_and_sell_qty_gt_0 = (mergedfo_df_filtered['qty'] > 0) & (mergedfo_df_filtered['day_sell_quantity'] > 0)
            condition_qty_eq_0 = mergedfo_df_filtered['qty'] == 0
            
            # Apply the conditions to set new_pnl_y
            mergedfo_df_filtered['new_pnl_y'] = np.where(
                condition_qty_gt_0_and_sell_qty_gt_0,
                (mergedfo_df_filtered['unrealised'] - mergedfo_df_filtered['PnL']).astype(int),
                np.where(
                    condition_qty_eq_0,
                    mergedfo_df_filtered['unrealised'],
                    mergedfo_df_filtered['unrealised']  # This handles any other case where qty > 0 but day_sell_quantity <= 0
                )
            )
            
            total_profit_fo = int(mergedfo_df_filtered['new_pnl_y'].sum())
            
            # Select relevant columns and save to CSV
            mergedfo_df_filtered = mergedfo_df_filtered[['tradingsymbol', 'new_pnl_y']]
            mergedfo_df_filtered.to_csv('pxyoptprofit.csv', index=False)
            
            formatted_str_fo = mergedfo_df_filtered.to_string(index=False, header=False)
            # Uncomment and adjust print formatting if needed
            # for line in formatted_str_fo.split('\n'):
            #     print(f"{line:>41}")
        else:
            #print("I did not exit any FNO positions today🤔🤔")
            empty_df = pd.DataFrame(columns=['tradingsymbol', 'new_pnl_y'])  # Ensure 'empty_df' is defined
            empty_df.to_csv('pxyoptprofit.csv', index=False)
        
        # Calculate and print total profit for NFO positions
        total_profit_all = total_profit_fo + total_profit
        # Uncomment and adjust print formatting if needed
        # print(f"{BRIGHT_GREEN}{'All Profits 💰 :' + str(total_profit_all):>41}{RESET}")
        
        return total_profit

    except Exception as e:
        logging.error(f"Error occurred in process_data_total_profit: {e}")
        print(f"An error occurred: {e}")
        traceback.print_exc()
        return 0

def main():
    try:
        process_data_total_profit()
    except Exception as e:
        logging.error(f"Error occurred in main: {e}")
        print(f"An error occurred in main: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    main()


