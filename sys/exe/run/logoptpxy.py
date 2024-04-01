import logging

def handle_order_placement_error(symbol, error):
    logging.error(f"Error placing order for {symbol}: {error}")

def log_telegram_error(error):
    logging.error(f"Error sending message to Telegram: {error}")

def setup_logging():
    logging.basicConfig(filename='trading.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

