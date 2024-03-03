def get_open_order_status(symbol):
    try:
        orders = broker.kite.orders()
        for order in orders:
            if order['status'] == 'OPEN' and order['tradingsymbol'] == symbol:
                return "YES"  # There is at least one open order for the symbol
    except Exception as e:
        remove_token(dir_path)
        logging.error(f"{str(e)} unable to get orders")
        sys.exit(1)
    return "NO"  # No open orders found for the symbol
