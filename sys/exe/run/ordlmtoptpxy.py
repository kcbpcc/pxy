import requests
import logging

def place_sell_limit_orders(exe_opt_df, broker):
    open_orders = {}
    missing_orders = []

    PROJECTED_TPL_PERCENTAGE = 10

    for index, row in exe_opt_df.iterrows():
        target_symbol = row['tradingsymbol']
        required_quantity = row['quantity']
        target_price = row['target_price']
        tPL_percentage = row['tPL%']

        if tPL_percentage >= PROJECTED_TPL_PERCENTAGE:
            if target_symbol not in open_orders:
                missing_orders.append(target_symbol)
                message = f"Placing order for {target_symbol} with quantity {required_quantity} and target price {target_price}"
                order_id = place_order(target_symbol, required_quantity, 'SELL', 'LIMIT', 'MIS', broker, message)
                if order_id:
                    open_orders[target_symbol] = order_id
                    print(f"Placed order for {target_symbol}.")
            else:
                print(f"Order already placed for {target_symbol}.")
                if open_orders.get(target_symbol):
                    print(f"Order ID for {target_symbol}: {open_orders[target_symbol]}")

    return open_orders

def place_order(symbol, quantity, order_type, price_type, order_mode, broker, message):
    try:
        response = requests.post(
            f"{broker.api_url}/orders",
            json={
                "symbol": symbol,
                "quantity": quantity,
                "order_type": order_type,
                "price_type": price_type,
                "order_mode": order_mode,
                "message": message
            }
        )
        if response.status_code == 201:
            return response.json().get("order_id")
        else:
            logging.error(f"Failed to place order for {symbol}, Status Code: {response.status_code}")
            return None
    except Exception as e:
        logging.error(f"Error while placing order for symbol {symbol}: {e}")
        return None
