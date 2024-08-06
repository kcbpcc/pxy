async def place_order(broker, symbol, transaction_type, product_type, quantity, order_type, price=None):
    def extract_strike(symbol):
        # Extract the last 5 digits from the symbol
        return int(symbol[-7:-2])  # Last 7 characters minus the last 2 (CE or PE)

    def generate_alternate_symbols(symbol):
        strike = extract_strike(symbol)
        if symbol.endswith("CE"):
            return [f"{strike + 100}CE"]
        elif symbol.endswith("PE"):
            return [f"{strike - 100}PE"]
        return []

    def attempt_order(symbol, transaction_type, product_type, quantity, order_type, price):
        try:
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

    # Attempt to place the initial order
    success, order_id = attempt_order(symbol, transaction_type, product_type, quantity, order_type, price)

    if not success:
        # If the initial order fails, try alternative strikes
        alternate_symbols = generate_alternate_symbols(symbol)
        for alt_symbol in alternate_symbols:
            success, order_id = attempt_order(alt_symbol, transaction_type, product_type, quantity, order_type, price)
            if success:
                print(f"Order placed successfully for alternative symbol: {alt_symbol}")
                return True, order_id
        print("All attempts to place order failed.")
        return False, None

    return True, order_id
