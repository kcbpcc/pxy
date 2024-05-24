import traceback
from login_get_kite import get_kite, remove_token
from cnstpxy import dir_path
from toolkit.logger import Logger
import logging

# Initialize logging
logging = Logger(30, dir_path + "main.log")

try:
    # Replace 'your_api_key' with your actual API key
    broker = get_kite(api_key="avku59f296gcvrv0", access_token="CTHBT6DLB6AEYZBQRN2KHABXB4GFPLCW", sec_dir=dir_path)
    
    # Retrieve holdings
    holdings = broker.holdings()
    
    if holdings:
        # Print holdings
        print("Holdings:")
        for holding in holdings:
            print(f"Instrument: {holding['tradingsymbol']}, Quantity: {holding['quantity']}, Average Price: {holding['average_price']}")
    else:
        print("No holdings found.")
except Exception as e:
    remove_token(dir_path)
    print(traceback.format_exc())
    logging.error(f"{str(e)} unable to get holdings")
    sys.exit(1)
