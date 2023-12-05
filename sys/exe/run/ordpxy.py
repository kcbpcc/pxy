import sys
from toolkit.logger import Logger
from login_get_kite import get_kite, remove_token
from cnstpxy import dir_path

# Configure logging
logging = Logger(30, dir_path + "main.log")

def list_all_orders():
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
        
        # Print information about each order
        for order in orders:
            print(f"Order ID: {order['order_id']}")
            print(f"Symbol: {order['tradingsymbol']}")
            print(f"Quantity: {order['quantity']}")
            print(f"Order Type: {order['order_type']}")
            print(f"Order Status: {order['status']}")
            print("---")

    except Exception as e:
        remove_token(dir_path)
        logging.error(f"{str(e)} unable to get orders")
        sys.exit(1)

# Call the function to list all orders
list_all_orders()
