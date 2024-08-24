import logging

def place_sell_limit_order(tradingsymbol, quantity, transaction_type, order_type, product, broker, message):
    try:
        order_id = broker.order_place(
            tradingsymbol=tradingsymbol,
            quantity=quantity,
            exchange='NFO',
            transaction_type=transaction_type,
            order_type=order_type,
            product=product
        )
        if order_id:  # Check if order_id is valid
            logging.info(f"Order placed successfully. Order ID: {order_id}")
            send_telegram_message(message)
            return order_id
        else:
            logging.error("Order placement failed. No valid order ID returned.")
            return None
    except Exception as e:
        logging.error(f"Error placing order: {e}")
        return None

def send_telegram_message(message):
    # Assuming this function sends a message to Telegram
    # Implement this function based on your requirements
    pass

