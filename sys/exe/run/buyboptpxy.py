import traceback
import sys
import logging
import telegram
import asyncio
from datetime import datetime, timedelta

# Importing necessary functions and constants
from login_get_kite import get_kite, remove_token
from cnstpxy import dir_path
from strikpxy import get_prices
from ordoptpxy import place_order
from macdpxy import calculate_macd_signal
from smapxy import check_index_status
from mktpxy import get_market_check
from rsnprntpxy import process_orders
from exprpxy import month_expiry_date
from bftpxy import get_bnk_action
from predictpxy import predict_market_sentiment
from bpredictpxy import predict_bnk_sentiment
from clorpxy import SILVER, UNDERLINE, RED, GREEN, YELLOW, RESET, BRIGHT_YELLOW, BRIGHT_RED, BRIGHT_GREEN, BOLD, GREY
from hndmktpxy import hand

# Get initial data
BCE_Strike, _, _, BPE_Strike = get_prices()
nsma = check_index_status('^NSEBANK')
onemincandlesequance, mktpxy = get_market_check('^NSEBANK')
ha_nse_action, nse_power, Day_Change, Open_Change = get_bnk_action()
mktpredict = predict_market_sentiment()
bmktpredict = predict_bnk_sentiment()
showhand = hand(mktpxy)

def construct_symbol(expiry_year, expiry_month, expiry_day, option_type):
    # Adjust month format if necessary
    if len(expiry_month) == 2 and expiry_month.startswith("0"):
        expiry_month = expiry_month[1]
    noptions = BPE_Strike if option_type == "PE" else (BCE_Strike if option_type == "CE" else None)
    if expiry_day is None:
        return f"BANKNIFTY{expiry_year}{expiry_month}{noptions}{option_type}"
    else:
        return f"BANKNIFTY{expiry_year}{expiry_month}{expiry_day}{noptions}{option_type}"

def count_positions_by_type(broker):
    positions_response = broker.kite.positions()
    positions_net = positions_response['net']
    count_CE = 0
    count_PE = 0
    for position in positions_net:
        if position['tradingsymbol'].startswith('BANK') and abs(position['quantity']) >= 15:
            if position['tradingsymbol'].endswith('CE'):
                count_CE += 1
            elif position['tradingsymbol'].endswith('PE'):
                count_PE += 1
    return count_CE, count_PE

def check_existing_positions(broker, symbol):
    positions_response = broker.kite.positions()
    positions_net = positions_response['net']
    for position in positions_net:
        if position['tradingsymbol'][-7:] == symbol[-7:] and abs(position['quantity']) >= 15:
            return True
    return False

async def main():
    try:
        # Redirect sys.stdout to 'output.txt'
        with open('output.txt', 'w') as file:
            sys.stdout = file

            try:
                broker = get_kite()
            except Exception as e:
                remove_token(dir_path)
                print(traceback.format_exc())
                logging.error(f"{str(e)} unable to get holdings")
                sys.exit(1)

    finally:
        # Reset sys.stdout to its default value
        sys.stdout = sys.__stdout__

    try:
        from fundpxy import calculate_decision
        decision, optdecision, available_cash, live_balance, limit = calculate_decision()

        count_CE, count_PE = count_positions_by_type(broker)
        PE_weight = count_PE - count_CE
        CE_weight = count_CE - count_PE
        weight = abs(count_PE - count_CE)

        print(f"{BRIGHT_YELLOW}{count_PE:02}📉:PE positions💧B-{showhand}🔥CE positions:📈{count_CE:02}{RESET}")

        expiry_year, expiry_month, expiry_day = month_expiry_date()

        CE_symbol = construct_symbol(expiry_year, expiry_month, expiry_day, 'CE')
        PE_symbol = construct_symbol(expiry_year, expiry_month, expiry_day, 'PE')

        CE_position_exists = check_existing_positions(broker, CE_symbol)
        PE_position_exists = check_existing_positions(broker, PE_symbol)

        if bmktpredict == "SIDE":
            if mktpxy == "Buy" and not CE_position_exists:
                await process_orders(broker, available_cash, CE_position_exists, False, CE_symbol, None, count_CE, count_PE, mktpxy)

            if mktpxy == "Sell" and not PE_position_exists:
                await process_orders(broker, available_cash, False, PE_position_exists, None, PE_symbol, count_CE, count_PE, mktpxy)

        elif bmktpredict == "RISE":
            if mktpxy == "Buy" and not CE_position_exists:
                await process_orders(broker, available_cash, CE_position_exists, False, CE_symbol, None, count_CE, count_PE, mktpxy)

            if mktpxy == "Sell" and not PE_position_exists and nse_power > 0.85:
                await process_orders(broker, available_cash, False, PE_position_exists, None, PE_symbol, count_CE, count_PE, mktpxy)

        elif bmktpredict == "FALL":
            if mktpxy == "Buy" and not CE_position_exists and nse_power < 0.15:
                await process_orders(broker, available_cash, CE_position_exists, False, CE_symbol, None, count_CE, count_PE, mktpxy)

            if mktpxy == "Sell" and not PE_position_exists:
                await process_orders(broker, available_cash, False, PE_position_exists, None, PE_symbol, count_CE, count_PE, mktpxy)

    except Exception as e:
        print(f"Error: {e}")
        logging.error(f"Error in main(): {e}")

async def run_main():
    await main()

# Run the asynchronous function using asyncio.run()
def sync_main():
    asyncio.run(run_main())

sync_main()



