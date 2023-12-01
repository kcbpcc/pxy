# funds.py
import sys
from toolkit.logger import Logger
from login_get_kite import get_kite, remove_token
from cnstpxy import dir_path

# Configure logging
logging = Logger(30, dir_path + "main.log")

def calculate_decision():
    try:
        # Assuming kite is defined in the get_kite function
        broker = get_kite(api="bypass", sec_dir=dir_path)
    except Exception as e:
        remove_token(dir_path)
        logging.error(f"{str(e)} unable to get broker")
        sys.exit(1)

    try:
        logging.debug("getting margin information ...")
        # Assuming kite is defined somewhere in the get_kite function
        # Use the 'margins' method to get margin data without specifying a segment
        response = broker.kite.margins()

        # Access the margin data from the response
        equity_info = response["equity"]
        used_margin = equity_info["utilised"]["debits"]
        net_margin = equity_info["net"]

        print(f"Used Margin: {used_margin}")
        print(f"Net Margin: {net_margin}")

        # Define 'YES' or 'NO' based on the margin conditions
        decision = "YES" if net_margin > 0 else "NO"

        return decision

    except Exception as e:
        remove_token(dir_path)
        logging.error(f"{str(e)} unable to get margin information")
        sys.exit(1)
