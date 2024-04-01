def check_existing_positions(broker, symbol):
    positions_response = broker.kite.positions()
    positions_net = positions_response['net']
    for position in positions_net:
        # Check if 'tradingsymbol' matches and 'quantity' is at least 50
        if position['tradingsymbol'] == symbol and position['quantity'] >= 50:
            return True
    return False
