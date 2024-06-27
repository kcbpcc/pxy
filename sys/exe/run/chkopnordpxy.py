import sys
import traceback
from login_get_kite import get_kite, remove_token
import logging

# Function to check and cancel orphan sell orders
def check_and_cancel_orphan_sell_orders(broker):
    try:
        # Fetch open orders and positions from broker
        open_orders = broker.orders()
        positions_response = broker.positions()
        positions_net = positions_response['net']

        # Collect all trading symbols with positive positions
        symbols_with_positions = {position['tradingsymbol'] for position in positions_net if position['quantity'] > 0}

        # Iterate through open orders to find orphan sell orders
        for order in open_orders:
            if order['transaction_type'] == 'SELL' and order['tradingsymbol'] in symbols_with_positions:
                # Order has a matching position, continue to next order
                continue

            # Cancel orphan sell orders
            cancel_result = broker.cancel_order(order['order_id'])
            if cancel_result:
                print(f"Cancelled orphan sell order {order['order_id']} for {order['tradingsymbol']}")
            else:
                print(f"Failed to cancel order {order['order_id']} for {order['tradingsymbol']}")

        # Check positions with positive quantity for target order placement
        for position in positions_net:
            if position['quantity'] > 0:
                # Fetch current market price for the symbol
                market_price = broker.ltp(position['tradingsymbol'])

                # Calculate average price
                avg_price = position['average_price']

                # Check if current price is at least 50% above average price
                if market_price >= 1.5 * avg_price:
                    # Keep the position, no action needed
                    print(f"Position for {position['tradingsymbol']} is at least 50% above average price. Keeping position.")
                else:
                    # Place target order for the position
                    target_quantity = position['quantity']
                    target_price = 1.5 * avg_price  # Place target at 50% above average price
                    place_order_result = broker.place_order(
                        tradingsymbol=position['tradingsymbol'],
                        quantity=target_quantity,
                        transaction_type='SELL',
                        order_type='LIMIT',
                        price=target_price,
                        product='MIS'  # Modify as per your broker's requirement
                    )
                    if place_order_result:
                        print(f"Target order placed successfully for {position['tradingsymbol']} at {target_price}")
                    else:
                        print(f"Failed to place target order for {position['tradingsymbol']}")

    except Exception as e:
        print(f"Error checking or cancelling orphan sell orders or placing target orders: {e}")

if __name__ == "__main__":
    try:
        # Redirect sys.stdout to 'output.txt'
        with open('output.txt', 'w') as file:
            sys.stdout = file

            try:
                # Get broker connection
                broker = get_kite()

                # Check and cancel orphan sell orders and place target orders
                check_and_cancel_orphan_sell_orders(broker)

            except Exception as e:
                # Handle exception
                remove_token()
                print(traceback.format_exc())
                logging.error(f"{str(e)} unable to check or cancel orphan sell orders or place target orders")
                sys.exit(1)

    finally:
        # Reset sys.stdout to its default value
        sys.stdout = sys.__stdout__
