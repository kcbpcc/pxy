adjust = 0
import traceback
import sys
import logging
import telegram
import asyncio
from login_get_kite import get_kite, remove_token
from cnstpxy import dir_path
from strikpxy import get_prices
from datetime import datetime, timedelta
from ordoptpxy import place_order
_, CE_Strike, PE_Strike, _ = get_prices()
from macdpxy import calculate_macd_signal
from smapxy import check_index_status
nsma = check_index_status('^NSEI')
from mktpxy import get_market_check
onemincandlesequance, mktpxy = get_market_check('^NSEI')
from rsnprntpxy import process_orders
from exprpxy import month_expiry_date
from hndmktpxy import hand
showhand = hand(mktpxy)
from nftpxy import ha_nse_action, nse_power, Day_Change, Open_Change
from predictpxy import predict_market_sentiment
from bpredictpxy import predict_bnk_sentiment
mktpredict = predict_market_sentiment()
bmktpredict = predict_bnk_sentiment()
from clorpxy import SILVER, UNDERLINE, RED, GREEN, YELLOW, RESET, BRIGHT_YELLOW, BRIGHT_RED, BRIGHT_GREEN, BOLD, GREY

print(f"Initial market prediction: {mktpredict}")

def construct_symbol(expiry_year, expiry_month, expiry_day, option_type, strike_price):
    if len(expiry_month) == 2 and expiry_month.startswith("0"):
        expiry_month = expiry_month[1]
    symbol = f"NIFTY{expiry_year}{expiry_month}{expiry_day}{strike_price}{option_type}"
    print(f"Constructed symbol: {symbol}")
    return symbol

def count_positions_by_type(broker):
    positions_response = broker.kite.positions()
    positions_net = positions_response['net']
    count_CE = 0
    count_PE = 0
    for position in positions_net:
        if position['tradingsymbol'].startswith('NIFTY') and abs(position['quantity']) >= 25:
            if position['tradingsymbol'].endswith('CE'):
                count_CE += 1
            elif position['tradingsymbol'].endswith('PE'):
                count_PE += 1
    print(f"Positions count - CE: {count_CE}, PE: {count_PE}")
    return count_CE, count_PE

def check_existing_positions(broker, symbol):
    positions_response = broker.kite.positions()
    positions_net = positions_response['net']
    for position in positions_net:
        if position['tradingsymbol'][-7:] == symbol[-7:] and abs(position['quantity']) >= 25:
            print(f"Position exists for symbol: {symbol}")
            return True
    print(f"Position does not exist for symbol: {symbol}")
    return False

async def main():
    try:
        # Redirect sys.stdout to 'output.txt'
        with open('output.txt', 'w') as file:
            sys.stdout = file

            try:
                broker = get_kite()
                print("Broker instance obtained successfully.")
            except Exception as e:
                remove_token(dir_path)
                print(traceback.format_exc())
                logging.error(f"{str(e)} unable to get holdings")
                print(f"Error obtaining broker instance: {e}")
                sys.exit(1)

    finally:
        # Reset sys.stdout to its default value
        sys.stdout = sys.__stdout__

    try:
        from fundpxy import calculate_decision
        decision, optdecision, available_cash, live_balance, limit = calculate_decision()
        print(f"Trading decision: {decision}, Option decision: {optdecision}")
        print(f"Available cash: {available_cash}, Live balance: {live_balance}, Limit: {limit}")

        count_CE, count_PE = count_positions_by_type(broker)
        PE_weight = count_PE - count_CE
        CE_weight = count_CE - count_PE
        weight = abs(count_PE - count_CE)
        print(f"PE weight: {PE_weight}, CE weight: {CE_weight}, Absolute weight difference: {weight}")

        expiry_year, expiry_month, expiry_day = month_expiry_date()
        print(f"Expiry date - Year: {expiry_year}, Month: {expiry_month}, Day: {expiry_day}")

        async def process_multiple_orders(symbols, option_type):
            print(f"Processing multiple orders for option type: {option_type}")
            for symbol in symbols:
                position_exists = check_existing_positions(broker, symbol)
                await process_orders(broker, available_cash, position_exists, position_exists, symbol, symbol, count_CE, count_PE, mktpxy) if mktpxy in ("Buy", "Sell") else None
                print(f"Processed order for symbol: {symbol}")

        if mktpredict == "RISE":
            CE_symbols = [construct_symbol(expiry_year, expiry_month, expiry_day, 'CE', CE_Strike + i) for i in [0, 100, 200, 300]]
            print(f"RISE strategy - CE symbols: {CE_symbols}")
            await process_multiple_orders(CE_symbols, "CE")
            PE_symbol = construct_symbol(expiry_year, expiry_month, expiry_day, 'PE', PE_Strike)
            PE_position_exists = check_existing_positions(broker, PE_symbol)
            print(f"RISE strategy - Processing PE symbol: {PE_symbol}")
            await process_orders(broker, available_cash, PE_position_exists, PE_position_exists, PE_symbol, PE_symbol, count_CE, count_PE, mktpxy) if mktpxy in ("Buy", "Sell") else None
        elif mktpredict == "FALL":
            PE_symbols = [construct_symbol(expiry_year, expiry_month, expiry_day, 'PE', PE_Strike - i) for i in [0, 100, 200, 300]]
            print(f"FALL strategy - PE symbols: {PE_symbols}")
            await process_multiple_orders(PE_symbols, "PE")
            CE_symbol = construct_symbol(expiry_year, expiry_month, expiry_day, 'CE', CE_Strike)
            CE_position_exists = check_existing_positions(broker, CE_symbol)
            print(f"FALL strategy - Processing CE symbol: {CE_symbol}")
            await process_orders(broker, available_cash, CE_position_exists, CE_position_exists, CE_symbol, CE_symbol, count_CE, count_PE, mktpxy) if mktpxy in ("Buy", "Sell") else None
        elif mktpredict == "SIDE":
            CE_symbol = construct_symbol(expiry_year, expiry_month, expiry_day, 'CE', CE_Strike)
            PE_symbol = construct_symbol(expiry_year, expiry_month, expiry_day, 'PE', PE_Strike)
            print(f"SIDE strategy - CE symbol: {CE_symbol}, PE symbol: {PE_symbol}")
            CE_position_exists = check_existing_positions(broker, CE_symbol)
            PE_position_exists = check_existing_positions(broker, PE_symbol)
            await process_orders(broker, available_cash, CE_position_exists, PE_position_exists, CE_symbol, PE_symbol, count_CE, count_PE, mktpxy) if mktpxy in ("Buy", "Sell") else None

    except Exception as e:
        print(f"Error: {e}")
        logging.error(f"Error in main(): {e}")

async def run_main():
    await main()

# Run the asynchronous function using asyncio.run()
def sync_main():
    asyncio.run(run_main())

sync_main()



