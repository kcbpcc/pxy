async def place_order(broker, symbol, transaction_type, product_type, quantity, order_type, price=None):
    try:
        if price is None:
            # Place market order if price is not specified
            order_id = broker.order_place(
                tradingsymbol=symbol,
                quantity=quantity,
                exchange="NFO",
                transaction_type=transaction_type,
                order_type=order_type,
                product=product_type
            )
            # Fetch executed price if it's a market order
            executed_price = broker.fetch_executed_price(order_id)
        else:
            # Place limit order if price is specified
            order_id = broker.order_place(
                tradingsymbol=symbol,
                quantity=quantity,
                exchange="NFO",
                transaction_type=transaction_type,
                order_type=order_type,
                product=product_type,
                price=price
            )
            executed_price = price  # Use provided price as executed price

        # Calculate 7% higher target price
        target_price = executed_price * 1.07  # 7% higher than executed price

        # Place limit target order
        target_order_id = broker.order_place(
            tradingsymbol=symbol,
            quantity=quantity,  # Same quantity as the initial buy order
            exchange="NFO",
            transaction_type='SELL',  # Assuming target is a sell order
            order_type='LIMIT',
            product=product_type,
            price=target_price
        )

        return True, order_id, target_order_id

    except Exception as e:
        print(f"Error placing order for {symbol}: {e}")
        return False, None, None

