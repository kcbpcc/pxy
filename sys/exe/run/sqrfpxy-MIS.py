import sys
from login_get_kite import get_kite, remove_token
from toolkit.logger import Logger
from cnstpxy import dir_path
from fundpxy import calculate_decision

############################################"PXY® PreciseXceleratedYield Pvt Ltd™###########################################
sys.stdout = open('output.txt', 'w')
logging = Logger(30, dir_path + "main.log")
try:
    broker = get_kite(api="bypass", sec_dir=dir_path)
    decision = calculate_decision()
except Exception as e:
    remove_token(dir_path)
    print(traceback.format_exc())
    logging.error(f"{str(e)} Unable to get holdings")
    sys.exit(1)
sys.stdout.close()
sys.stdout = sys.__stdout__
############################################"PXY® PreciseXceleratedYield Pvt Ltd™###########################################

def close_all_mis_positions():
    try:
        # Get all existing positions
        positions = broker.positions()

        for position in positions:
            # Check for MIS (Margin Intraday Square-off) positions
            if position['product'] == 'MIS' and position['quantity'] < 0:
                # Place a market buy order to close the MIS sell position
                order_id = broker.order_place(
                    tradingsymbol=position['tradingsymbol'],
                    exchange=position['exchange'],
                    transaction_type='BUY',
                    quantity=abs(position['quantity']),
                    order_type='MARKET',
                    product=position['product'],
                    variety=position['variety'],
                    price=None
                )

                if order_id:
                    logging.info(f"Market Buy Order {order_id} placed successfully to close MIS sell position")
                else:
                    logging.error("Market Buy Order placement failed")
    except Exception as e:
        logging.error(f"{str(e)} Unable to close MIS positions")

# Close all existing MIS positions
close_all_mis_positions()
