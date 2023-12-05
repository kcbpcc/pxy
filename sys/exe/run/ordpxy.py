import sys
from toolkit.logger import Logger
from login_get_kite import get_kite, remove_token
from cnstpxy import dir_path

# Configure logging
logging = Logger(30, dir_path + "main.log")

def list_open_orders():
    try:
        # Assuming kite is defined in the get_kite function
        broker = get_kite(api="bypass", sec_dir=dir_path)
    except Exception as e:
        remove_token(dir_path)
        logging.error(f"{str(e)} unable to get broker")
        sys.exit(1)

    try:
        # Assuming kite is defined somewhere in the get_kite function
        # Use the 'orders' method to get a list of all orders
        orders = broker.kite.orders()

        # Print information about open orders
        for order in orders:
            if order['status'] == 'OPEN':
                print(f"Symbol: {order['tradingsymbol']}")
                print(f"Order Status: {order['status']}")
                print("---")

    except Exception as e:
        remove_token(dir_path)
        logging.error(f"{str(e)} unable to get orders")
        sys.exit(1)

# Call the function to list open orders
list_open_orders()
