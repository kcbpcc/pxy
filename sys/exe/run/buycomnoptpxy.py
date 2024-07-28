import logging
import sys
from login_get_kite import get_kite, remove_token
from cnstpxy import dir_path
from strikpxy import get_prices
from ordoptpxy import place_order
from mktpxy import get_market_check
from rsnprntpxy import process_orders
from exprpxy import month_expiry_date
from clorpxy import SILVER, UNDERLINE, RED, GREEN, YELLOW, RESET, BRIGHT_YELLOW, BRIGHT_RED, BRIGHT_GREEN, BOLD, GREY
from predictpxy import predict_market_sentiment
from fundpxy import calculate_decision
from bpredictpxy import predict_bnk_sentiment

# Common Constants
mktpredict = predict_market_sentiment()

def construct_symbols(expiry_year, expiry_month, expiry_day, option_type, strike_price):
    symbols = []
    if option_type == "CE":
        symbols.append(f"NIFTY{expiry_year}{expiry_month}{expiry_day}{strike_price}CE")
        symbols.append(f"NIFTY{expiry_year}{expiry_month}{expiry_day}{strike_price+100}CE")
        symbols.append(f"NIFTY{expiry_year}{expiry_month}{expiry_day}{strike_price+200}CE")
    elif option_type == "PE":
        symbols.append(f"NIFTY{expiry_year}{expiry_month}{expiry_day}{strike_price}PE")
        symbols.append(f"NIFTY{expiry_year}{expiry_month}{expiry_day}{strike_price-100}PE")
        symbols.append(f"NIFTY{expiry_year}{expiry_month}{expiry_day}{strike_price-200}PE")
    return symbols

def construct_symbol(expiry_year, expiry_month, expiry_day, option_type, strike_price):
    if len(expiry_month) == 2 and expiry_month.startswith("0"):
        expiry_month = expiry_month[1]
    return f"BANKNIFTY{expiry_year}{expiry_month}{expiry_day}{strike_price}{option_type}"

def count_positions_by_type(broker, instrument_type, min_qty):
    positions_response = broker.kite.positions()
    positions_net = positions_response['net']
    count_CE = 0
    count_PE = 0
    for position in positions_net:
        if position['tradingsymbol'].startswith(instrument_type) and abs(position['quantity']) >= min_qty:
            if position['tradingsymbol'].endswith('CE'):
                count_CE += 1
            elif position['tradingsymbol'].endswith('PE'):
                count_PE += 1
    return count_CE, count_PE

def check_existing_positions(broker, symbol, min_qty):
    positions_response = broker.kite.positions()
    positions_net = positions_response['net']
    for position in positions_net:
        if position['tradingsymbol'][-7:] == symbol[-7:] and abs(position['quantity']) >= min_qty:
            return True
    return False
