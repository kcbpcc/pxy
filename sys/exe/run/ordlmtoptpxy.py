import requests
import logging

def place_sell_limit_orders(lmt_ord_df, broker):
    """Place sell limit orders for each row in the DataFrame."""
    open_orders = {}
    for index, row in lmt_ord_df.iterrows():
        try:
            response = requests.post(f"{broker.api_url}/orders", json={
                'tradingsymbol': row['tradingsymbol'],
                'quantity': row['quantity'],
                'price': row['target_price'],
                'order_type': 'LIMIT',
                'transaction_type': 'SELL',
                'product': 'NRML'
            })
            if response.status_code == 200:
                order_id = response.json().get('order_id')
                if order_id:
                    open_orders[row['tradingsymbol']] = {'order_id': order_id, 'quantity': row['quantity']}
                    print(f"Order placed successfully for symbol: {row['tradingsymbol']}")
                else:
                    print(f"Failed to place order for symbol: {row['tradingsymbol']}")
            else:
                print(f"Failed to place order for symbol: {row['tradingsymbol']}, Status Code: {response.status_code}")
        except Exception as e:
            print(f"Error placing order for symbol {row['tradingsymbol']}: {e}")
    return open_orders

