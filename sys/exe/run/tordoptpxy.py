# order_management.py
import requests

from kiteconnect import KiteConnect

def get_ltp(kite: KiteConnect, tradingsymbol: str) -> float:
    try:
        # Fetch the market quote for the given symbol
        quote = kite.quote(f'NFO:{tradingsymbol}')
        ltp = quote[f'NFO:{tradingsymbol}']['last_price']
        return ltp
    except Exception as e:
        print(f"Error fetching LTP for {tradingsymbol}: {e}")
        return None

def has_open_orders(kite: KiteConnect, tradingsymbol: str) -> bool:
    try:
        # Fetch all orders
        all_orders = kite.orders()
        # Filter orders to find open orders for the given tradingsymbol
        open_orders = [order for order in all_orders if order['tradingsymbol'] == tradingsymbol and order['status'] in ('OPEN', 'TRIGGER PENDING')]
        return len(open_orders) > 0
    except Exception as e:
        print(f"Error checking open orders for {tradingsymbol}: {e}")
        return False

def place_order(tradingsymbol, quantity, transaction_type, order_type, product, broker, message, bot_token, user_usernames, tgtoptsmadepth):
    # Print tgtoptsmadepth for debugging
    print(f"Target Options Market Depth: {tgtoptsmadepth}")

    # Check if there are open orders for the symbol
    if has_open_orders(broker, tradingsymbol):
        print(f"There are already open orders for {tradingsymbol}. Order not placed.")
        return None

    # Get the LTP using Zerodha Kite API
    ltp = get_ltp(broker, tradingsymbol)
    if ltp is None:
        print("Failed to fetch LTP. Order not placed.")
        return None
    
    # Determine the order type and price based on tgtoptsmadepth
    if tgtoptsmadepth <= 5:
        # Place a market order
        order_type = "MARKET"
        price = None
    else:
        # Place a limit order with a price 5% higher than the LTP
        order_type = "LIMIT"
        price = ltp * 1.14

    try:
        # Place the order
        order_id = broker.order_place(
            tradingsymbol=tradingsymbol,
            quantity=quantity,
            exchange='NFO',
            transaction_type=transaction_type,
            order_type=order_type,
            product=product,
            price=price if order_type == "LIMIT" else None  # Specify the limit price if it's a LIMIT order
        )
        if order_id:  # Check if order_id is valid
            print(f"Order placed successfully. Order ID: {order_id}")
            send_telegram_message(message, bot_token, user_usernames)
            return order_id
        else:
            print("Order placement failed. No valid order ID returned.")
            return None
    except Exception as e:
        print(f"Error placing order: {e}")
        return None
