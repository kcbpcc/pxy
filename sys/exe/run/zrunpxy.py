import sys
import traceback
from login_get_kite import get_kite, remove_token
from cnstpxy import dir_path
from toolkit.logger import Logger
import logging

# Initialize logging
logging = Logger(30, dir_path + "main.log")

try:
    sys.stdout = open('output.txt', 'w')
    # Replace 'your_api_key' with your actual API key
    broker = get_kite(api_key="avku59f296gcvrv0", access_token="CTHBT6DLB6AEYZBQRN2KHABXB4GFPLCW", sec_dir=dir_path)
    
    # Retrieve holdings
    holdings = broker.holdings()
    
    # Print holdings
    print("Holdings:")
    for holding in holdings:
        print(f"Instrument: {holding['tradingsymbol']}, Quantity: {holding['quantity']}, Average Price: {holding['average_price']}")
except Exception as e:
    remove_token(dir_path)
    print(traceback.format_exc())
    logging.error(f"{str(e)} unable to get holdings")
    sys.exit(1)
finally:
    # Ensure to close the file and restore stdout
    if sys.stdout != sys.__stdout__:
        sys.stdout.close()
        sys.stdout = sys.__stdout__
