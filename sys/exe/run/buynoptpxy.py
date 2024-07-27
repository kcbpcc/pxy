import traceback
import sys
import logging
import asyncio
from datetime import datetime, timedelta
from login_get_kite import get_kite, remove_token
from cnstpxy import dir_path
from strikpxy import get_prices
from ordoptpxy import place_order
from macdpxy import calculate_macd_signal
from smapxy import check_index_status
from mktpxy import get_market_check
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

bnkmaxcount = 15
nftmaxcount = 24

async def process_orders(broker, available_cash, CE_position_exists, PE_position_exists, CE_symbol, PE_symbol, count_CE, count_PE, mktpxy):
    from ordoptpxy import place_order
    from telinoptpxy import send_telegram_message

    try:
        # Proceed with order handling without checking funds
        await handle_CE_orders(broker, CE_position_exists, CE_symbol, count_CE, mktpxy, place_order, send_telegram_message, bnkmaxcount, nftmaxcount, bmktpredict)
        await handle_PE_orders(broker, PE_position_exists, PE_symbol, count_PE, mktpxy, place_order, send_telegram_message, bnkmaxcount, nftmaxcount, bmktpredict)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        logging.error(f"An error occurred: {str(e)}")

async def handle_CE_orders(broker, CE_position_exists, CE_symbol, count_CE, mktpxy, place_order, send_telegram_message, bnkmaxcount, nftmaxcount, bmktpredict):
    if not CE_position_exists and mktpxy == 'Buy':
        quantity = determine_quantity(CE_symbol, count_CE, 'BANKNIFTY', 'NIFTY', bnkmaxcount, nftmaxcount, bmktpredict)
        if quantity > 0:
            await execute_order(broker, CE_symbol, quantity, place_order, send_telegram_message)
            print_order_reason(CE_symbol, CE_position_exists, count_CE, 'Hold')
        else:
            print(f"Not placing order for {CE_symbol} as it is maxed out.")
    else:
        print_order_reason(CE_symbol, CE_position_exists, count_CE, 'Hold')

async def handle_PE_orders(broker, PE_position_exists, PE_symbol, count_PE, mktpxy, place_order, send_telegram_message, bnkmaxcount, nftmaxcount, bmktpredict):
    if not PE_position_exists and mktpxy == 'Sell':
        quantity = determine_quantity(PE_symbol, count_PE, 'BANKNIFTY', 'NIFTY', bnkmaxcount, nftmaxcount, bmktpredict)
        if quantity > 0:
            await execute_order(broker, PE_symbol, quantity, place_order, send_telegram_message)
        else:
            print(f"Not placing order for {PE_symbol} as it is maxed out.")
    else:
        print_order_reason(PE_symbol, PE_position_exists, count_PE, 'Hold')

def determine_quantity(symbol, count, banknifty_prefix, nifty_prefix, bnkmaxcount, nftmaxcount, bmktpredict):
    if symbol.startswith(banknifty_prefix) and count < bnkmaxcount:
        if symbol.endswith("PE") and bmktpredict == "FALL":
            return 15
        elif symbol.endswith("CE") and bmktpredict == "RISE":
            return 15
        else:
            return 15
    elif symbol.startswith(nifty_prefix) and count < nftmaxcount:
        return 25
    else:
        return 0

async def execute_order(broker, symbol, quantity, place_order, send_telegram_message):
    try:
        buy_order_placed, buy_order_id = await place_order(broker, symbol, 'BUY', 'NRML', quantity, 'MARKET')
        if buy_order_placed:
            await send_telegram_message(f"🛫🛫🛫 🌱🌱🌱 ENTRY order placed for {symbol} successfully.")
            print(f"{symbol} BUY order placed successfully.")
        else:
            print(f"Failed to place BUY order for {symbol}")
    except Exception as e:
        print(f"Error executing order for {symbol}: {e}")
        logging.error(f"Error executing order for {symbol}: {e}")

def print_order_reason(symbol, position_exists, count, action):
    reason = f"|{action}|{'🥚' if position_exists else '🧺'}|"
    reason += " MaxedOut" if count >= (bnkmaxcount if symbol.startswith('BANKNIFTY') else nftmaxcount) else ""
    if reason:
        print(f"{symbol}: {reason: >{39 - len(symbol)}}")

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

        count_CE, count_PE = count_positions_by_type(broker)
        print(f"Positions count - CE: {count_CE}, PE: {count_PE}")

        expiry_year, expiry_month, expiry_day = month_expiry_date()
        print(f"Expiry date - Year: {expiry_year}, Month: {expiry_month}, Day: {expiry_day}")

        async def process_multiple_orders(symbols, option_type):
            print(f"Processing multiple orders for option type: {option_type}")
            for symbol in symbols:
                position_exists = check_existing_positions(broker, symbol)
                await process_orders(broker, available_cash, position_exists, position_exists, symbol, symbol, count_CE, count_PE, mktpxy) 
                print(f"Processed order for symbol: {symbol}")

        if mktpredict == "RISE":
            CE_symbols = [construct_symbol(expiry_year, expiry_month, None, str(CE_Strike + i), 'CE') for i in [0, 100, 200]]
            print(f"RISE strategy - CE symbols: {CE_symbols}")
            await process_multiple_orders(CE_symbols, "CE")

            PE_symbol = construct_symbol(expiry_year, expiry_month, None, str(PE_Strike - 100), 'PE')
            print(f"RISE strategy - PE symbol: {PE_symbol}")
            await process_multiple_orders([PE_symbol], "PE")

        elif mktpredict == "FALL":
            PE_symbols = [construct_symbol(expiry_year, expiry_month, None, str(PE_Strike - i), 'PE') for i in [0, 100, 200]]
            print(f"FALL strategy - PE symbols: {PE_symbols}")
            await process_multiple_orders(PE_symbols, "PE")

            CE_symbol = construct_symbol(expiry_year, expiry_month, None, str(CE_Strike + 100), 'CE')
            print(f"FALL strategy - CE symbol: {CE_symbol}")
            await process_multiple_orders([CE_symbol], "CE")

        else:
            print(f"Market prediction '{mktpredict}' not recognized for placing orders.")

    except Exception as e:
        print(f"An error occurred during main execution: {e}")
        logging.error(f"An error occurred during main execution: {e}")

if __name__ == "__main__":
    asyncio.run(main())


