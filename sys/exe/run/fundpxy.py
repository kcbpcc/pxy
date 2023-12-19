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

        # Assuming kite is defined somewhere in the get_kite function
        # Use the 'margins' method to get margin data without specifying a segment
        response = broker.kite.margins()

        # Access the available cash from the response
        available_cash = response["equity"]["available"]["live_balance"]
        print(f"Available Cash: {available_cash}")
        # Define 'YES' or 'NO' based on the available cash
        decision = "YES" if available_cash > 100000 else "NO"

        return decision
        return available_cash
        print(available_cash)
    
    except Exception as e:
        remove_token(dir_path)
        logging.error(f"{str(e)} unable to get available cash")
        sys.exit(1)
