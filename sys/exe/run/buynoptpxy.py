import traceback
import sys
import logging
import asyncio
from login_get_kite import get_kite, remove_token
from cnstpxy import dir_path
from strikpxy import get_prices
from datetime import datetime, timedelta
from ordoptpxy import place_order
from macdpxy import calculate_macd_signal
from smapxy import check_index_status
from mktpxy import get_market_check
from rsnprntpxy import process_orders
from exprpxy import month_expiry_date
from hndmktpxy import hand
from nftpxy import ha_nse_action, nse_power, Day_Change, Open_Change
from predictpxy import predict_market_sentiment
from bpredictpxy import predict_bnk_sentiment
from clorpxy import SILVER, UNDERLINE, RED, GREEN, YELLOW, RESET, BRIGHT_YELLOW, BRIGHT_RED, BRIGHT_GREEN, BOLD, GREY

# Initialize various modules and settings
_, CE_Strike, PE_Strike, _ = get_prices()
nsma = check_index_status('^NSEI')
onemincandlesequance, mktpxy = get_market_check('^NSEI')
showhand = hand(mktpxy)
mktpredict = predict_market_sentiment()
bmktpredict = predict_bnk_sentiment()

def construct_symbol(expiry_year, expiry_month, expiry_day, strike_price, option_type):
    if len(expiry_month) == 2 and expiry_month.startswith("0"):
        expiry_month = expiry_month[1]
    if expiry_day is None:
        return f"NIFTY{expiry_year}{expiry_month}{strike_price}{option_type}"
    else:
        return f"NIFTY{expiry_year}{expiry_month}{expiry_day}{strike_price}{option_type}"

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
    return count_CE, count_PE

def check_existing_positions(broker, symbol):
    positions_response = broker.kite.positions()
    positions_net = positions_response['net']
    for position in positions_net:
        if position['tradingsymbol'][-7:] == symbol[-7:] and abs(position['quantity']) >= 25:
            return True
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

        # Print the trading decision and other details
        # print(f"Trading decision: {decision}, Option decision: {optdecision}")
        # print(f"Available cash: {available_cash}, Live balance: {live_balance}, Limit: {limit}")

        count_CE, count_PE = count_positions_by_type(broker)
        print(f"Positions count - CE: {count_CE}, PE: {count_PE}")

        expiry_year, expiry_month, expiry_day = month_expiry_date()
        print(f"Expiry date - Year: {expiry_year}, Month: {expiry_month}, Day: {expiry_day}")

        async def process_multiple_orders(symbols, option_type):
            print(f"Processing multiple orders for option type: {option_type}")
            for symbol in symbols:
                position_exists = check_existing_positions(broker, symbol)
                await process_orders(broker, available_cash, position_exists, position_exists, symbol, symbol, count_CE, count_PE, mktpxy) if mktpxy in ("Buy", "Sell") else None
                print(f"Processed order for symbol: {symbol}")

        if mktpredict == "RISE":
            CE_symbols = [construct_symbol(expiry_year, expiry_month, None, str(CE_Strike + i), 'CE') for i in [0, 100, 200]]
            print(f"RISE strategy - CE symbols: {CE_symbols}")
            await process_multiple_orders(CE_symbols, "CE")

            PE_symbol = construct_symbol(expiry_year, expiry_month, None, str(PE_Strike), 'PE')
            print(f"RISE strategy - Processing PE symbol: {PE_symbol}")
            PE_position_exists = check_existing_positions(broker, PE_symbol)
            await process_orders(broker, available_cash, PE_position_exists, PE_position_exists, PE_symbol, PE_symbol, count_CE, count_PE, mktpxy) if mktpxy in ("Buy", "Sell") else None

        elif mktpredict == "FALL":
            PE_symbols = [construct_symbol(expiry_year, expiry_month, None, str(PE_Strike - i), 'PE') for i in [0, 100, 200]]
            print(f"FALL strategy - PE symbols: {PE_symbols}")
            await process_multiple_orders(PE_symbols, "PE")

            CE_symbol = construct_symbol(expiry_year, expiry_month, None, str(CE_Strike), 'CE')
            print(f"FALL strategy - Processing CE symbol: {CE_symbol}")
            CE_position_exists = check_existing_positions(broker, CE_symbol)
            await process_orders(broker, available_cash, CE_position_exists, CE_position_exists, CE_symbol, CE_symbol, count_CE, count_PE, mktpxy) if mktpxy in ("Buy", "Sell") else None

        elif mktpredict == "SIDE":
            CE_symbol = construct_symbol(expiry_year, expiry_month, None, str(CE_Strike), 'CE')
            PE_symbol = construct_symbol(expiry_year, expiry_month, None, str(PE_Strike), 'PE')
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




