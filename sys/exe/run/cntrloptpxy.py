from toolkit.logger import Logger
from login_get_kite import get_kite, remove_token
import traceback
import pandas as pd

# Initialize logger
logging = Logger(30, "main.log")

try:
    # Get Kite instance
    broker = get_kite(api="bypass", sec_dir="dir_path")

except Exception as e:
    # Log error and exit
    remove_token("dir_path")
    logging.error(f"Unable to get holdings: {str(e)}")
    sys.exit(1)

def get_positionsinfo(resp_list, broker):
    try:
        # Convert response to DataFrame
        df = pd.DataFrame(resp_list)
        df['source'] = 'positions'
        return df
    except Exception as e:
        logging.error(f"An error occurred in positions: {e}")
        return None

try:
    # Fetch positions
    positions_response = broker.kite.positions()['net']

    # Convert response to DataFrame
    positions_df = get_positionsinfo(positions_response, broker)

    # Filter positions DataFrame to include only symbols containing "NIFTY"
    nifty_positions_df = positions_df[positions_df['tradingsymbol'].str.contains("NIFTY")]

    # Print filtered DataFrame
    print("NIFTY Positions DataFrame:")
    print(nifty_positions_df)

except Exception as e:
    # Log error and exit
    logging.error(f"Error in main loop: {str(e)}")
    remove_token("dir_path")
    traceback.print_exc()
    sys.exit(1)

