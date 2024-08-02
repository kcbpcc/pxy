async def place_order(broker, symbol, transaction_type, product_type, quantity, order_type, price=None):
    try:
        # Fetch existing orders
        existing_orders = broker.orders()
        symbol_orders = [order for order in existing_orders if order['tradingsymbol'] == symbol]
        
        if symbol_orders:
            print(f"Existing orders found for {symbol}: {symbol_orders}")
            return False, None

        # Place new order
        if price is None:
            order_id = broker.order_place(
                tradingsymbol=symbol,
                quantity=quantity,
                exchange="NFO",
                transaction_type=transaction_type,
                order_type=order_type,
                product=product_type
            )
        else:
            order_id = broker.order_place(
                tradingsymbol=symbol,
                quantity=quantity,
                exchange="NFO",
                transaction_type=transaction_type,
                order_type=order_type,
                product=product_type,
                price=price
            )
        
        return True, order_id
    except Exception as e:
        print(f"Error placing order for {symbol}: {e}")
        return False, None
