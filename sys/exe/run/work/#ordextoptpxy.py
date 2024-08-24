import logging

def cancel_existing_orders(symbol, broker):
    try:
        # Example method, update according to actual API
        response = broker.cancel_order(symbol=symbol)
        if response:
            logging.info(f"Cancelled existing open orders for symbol: {symbol}")
            return True
        else:
            logging.error(f"Failed to cancel orders for symbol: {symbol}")
            return False
    except Exception as e:
        logging.error(f"Error while cancelling orders for symbol {symbol}: {e}")
        return False

def exit_position(symbol, broker):
    try:
        # Example method, update according to actual API
        response = broker.exit_order(symbol=symbol)
        if response:
            logging.info(f"Exited position for symbol: {symbol}")
            return True
        else:
            logging.error(f"Failed to exit position for symbol: {symbol}")
            return False
    except Exception as e:
        logging.error(f"Error while exiting position for symbol {symbol}: {e}")
        return False
