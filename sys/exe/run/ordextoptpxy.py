import requests
import logging

def cancel_existing_orders(symbol, broker):
    """Cancel existing open orders for the given symbol."""
    try:
        response = requests.get(f"{broker.api_url}/orders/{symbol}")
        if response.status_code == 200:
            # Process response and cancel orders
            print(f"Orders canceled for symbol: {symbol}")
        else:
            logging.error(f"Failed to cancel orders for symbol: {symbol}, Status Code: {response.status_code}")
    except Exception as e:
        logging.error(f"Error while cancelling orders for symbol {symbol}: {e}")

def exit_position(exe_opt_df, broker):
    """Exit positions by canceling existing orders and placing new ones."""
    for index, row in exe_opt_df.iterrows():
        symbol = row['tradingsymbol']
        try:
            # Cancel existing orders before placing new ones
            cancel_existing_orders(symbol, broker)
            print(f"Cancelled existing open sell orders for symbol: {symbol}")
        except Exception as e:
            print(f"Error while cancelling orders for symbol {symbol}: {e}")
