import logging

def send_telegram_message(message):
    try:
        for username in user_usernames:
            url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
            payload = {'chat_id': username, 'text': message}
            response = requests.post(url, data=payload)
            if response.status_code != 200:
                print(f"Failed to send Telegram message. Status code: {response.status_code}")
            else:
                print("Telegram message sent successfully.")
    except Exception as e:
        print(f"Error sending Telegram message: {e}")

def get_ltp(broker, tradingsymbol: str) -> float:
    try:
        # Fetch the LTP for the given symbol using broker.kite.ltp
        ltp = broker.kite.ltp(f'NFO:{tradingsymbol}')[f'NFO:{tradingsymbol}']['last_price']
        return ltp
    except Exception as e:
        logging.error(f"Error fetching LTP for {tradingsymbol}: {e}")
        return None

def has_open_orders(broker, tradingsymbol: str) -> bool:
    try:
        # Fetch all orders
        all_orders = broker.kite.orders()
        # Filter orders to find open orders for the given tradingsymbol
        open_orders = [order for order in all_orders if order['tradingsymbol'] == tradingsymbol and order['status'] in ('OPEN', 'TRIGGER PENDING')]
        return len(open_orders) > 0
    except Exception as e:
        logging.error(f"Error checking open orders for {tradingsymbol}: {e}")
        return False

def place_order(tradingsymbol, quantity, transaction_type, order_type, product, message, bot_token, user_usernames, tgtoptsmadepth, broker):
    try:
        # Get the LTP using broker.kite.ltp
        ltp = get_ltp(broker, tradingsymbol)
        if ltp is None:
            logging.error("Failed to fetch LTP. Order not placed.")
            return None

        # Check if there are open orders for the symbol
        if has_open_orders(broker, tradingsymbol):
            logging.info(f"There are already open orders for {tradingsymbol}. Order not placed.")
            return None

        # Determine the order type and price based on tgtoptsmadepth
        if tgtoptsmadepth <= 5:
            # Place a market order
            order_type = "MARKET"
            price = None
        else:
            # Place a limit order with a price 5% higher than the LTP
            order_type = "LIMIT"
            price = ltp * 1.05

        try:
            # Place the order
            order_id = broker.kite.order_place(
                tradingsymbol=tradingsymbol,
                quantity=quantity,
                exchange='NFO',
                transaction_type=transaction_type,
                order_type=order_type,
                product=product,
                price=price if order_type == "LIMIT" else None  # Specify the limit price if it's a LIMIT order
            )
            if order_id:  # Check if order_id is valid
                logging.info(f"Order placed successfully. Order ID: {order_id}")
                send_telegram_message(message, bot_token, user_usernames)
                return order_id
            else:
                logging.error("Order placement failed. No valid order ID returned.")
                return None
        except Exception as e:
            logging.error(f"Error placing order: {e}")
            return None
    except Exception as e:
        logging.error(f"Error in place_order function: {e}")
        return None
