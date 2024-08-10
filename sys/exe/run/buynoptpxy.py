# final ...
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
from rsnprntpxy import process_orders
from exprpxy import month_expiry_date
from nftpxy import get_nse_action
from predictpxy import predict_market_sentiment
from clorpxy import SILVER, UNDERLINE, RED, GREEN, YELLOW, RESET, BRIGHT_YELLOW, BRIGHT_RED, BRIGHT_GREEN, BOLD, GREY
from hndmktpxy import hand

# Configure logging
logging.basicConfig(filename='error.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

# Get initial data
_, CE_Strike, PE_Strike, _ = get_prices()
nsma = check_index_status('^NSEI')
onemincandlesequance, mktpxy = get_market_check('^NSEI')
ha_nse_action, nse_power, Day_Change, Open_Change = get_nse_action()
mktpredict = predict_market_sentiment()
showhand = hand(mktpxy)

def construct_symbol(expiry_year, expiry_month, expiry_day, option_type):
    if len(expiry_month) == 2 and expiry_month.startswith("0"):
        expiry_month = expiry_month[1]
    noptions = PE_Strike if option_type == "PE" else (CE_Strike if option_type == "CE" else None)
    if expiry_day is None:
        return f"NIFTY{expiry_year}{expiry_month}{noptions}{option_type}"
    else:
        return f"NIFTY{expiry_year}{expiry_month}{noptions}{option_type}"

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
            # sys.stdout = file

            try:
                sys.stdout = file
                broker = get_kite()
                sys.stdout = sys.__stdout__
            except Exception as e:
                remove_token(dir_path)
                print(traceback.format_exc())
                logging.error(f"{str(e)} unable to get holdings")
                sys.exit(1)

            try:
                from fundpxy import calculate_decision
                decision, optdecision, available_cash, live_balance, limit = calculate_decision()
                count_CE, count_PE = count_positions_by_type(broker)
                PE_weight = count_PE - count_CE
                CE_weight = count_CE - count_PE
                weight = abs(count_PE - count_CE)
                strike_price = CE_Strike
                print(f"{BRIGHT_YELLOW}{count_PE:02} 📉:PE   ━━━━ {strike_price} | {showhand} ━━━━   CE:📈 {count_CE:02}{RESET}")

                expiry_year, expiry_month, expiry_day = month_expiry_date()

                CE_symbol = construct_symbol(expiry_year, expiry_month, expiry_day, 'CE')
                PE_symbol = construct_symbol(expiry_year, expiry_month, expiry_day, 'PE')

                CE_position_exists = check_existing_positions(broker, CE_symbol)
                PE_position_exists = check_existing_positions(broker, PE_symbol)

                def qty_positions_by_type(broker, CE_symbol, PE_symbol):
                    positions_response = broker.kite.positions()
                    positions_net = positions_response['net']
                    qty_CE = 0
                    qty_PE = 0
                    
                    for position in positions_net:
                        if position['tradingsymbol'] == CE_symbol:
                            qty_CE += int(abs(position['quantity']) / 25)
                        elif position['tradingsymbol'] == PE_symbol:
                            qty_PE += int(abs(position['quantity']) / 25)
                   
                    return qty_CE, qty_PE
                qty_CE, qty_PE = qty_positions_by_type(broker, CE_symbol, PE_symbol)

                # Print all relevant variables before entering the if block
                #print(f"bmktpredict: {bmktpredict}")
                #print(f"mktpxy: {mktpxy}")
                #print(f"CE_position_exists: {CE_position_exists}")
                print(f"{CE_symbol}                    {(f'{qty_CE}x' if CE_position_exists else '')}{'🥚' if CE_position_exists else '🛒'}".rjust(41))
                print(f"{PE_symbol}                    {(f'{qty_PE}x' if PE_position_exists else '')}{'🥚' if PE_position_exists else '🛒'}".rjust(41))
                #print(f"count_CE: {count_CE}")
                #print(f"count_PE: {count_PE}")
                

                if mktpredict == "SIDE":
                    if mktpxy == "Buy":
                        if CE_position_exists:
                            print(f"    {CE_symbol} is there, let's {BRIGHT_YELLOW}skip{RESET}")
                        else:
                            print(f"    {CE_symbol} not there, let's Buy")
                            await process_orders(broker, available_cash, CE_position_exists, False, CE_symbol, None, count_CE, count_PE, mktpxy)
                
                    elif mktpxy == "Sell":
                        if PE_position_exists:
                            print(f"    {PE_symbol} is there, let's {BRIGHT_YELLOW}skip{RESET}")
                        else:
                            print(f"    {PE_symbol} not there, let's Buy")
                            await process_orders(broker, available_cash, False, PE_position_exists, None, PE_symbol, count_CE, count_PE, mktpxy)
                
                elif mktpredict == "RISE":
                    if mktpxy == "Buy":
                        if CE_position_exists:
                            print(f"    {CE_symbol} is there, let's {BRIGHT_YELLOW}skip{RESET}")
                        else:
                            print(f"    {CE_symbol} not there, let's Buy")
                            await process_orders(broker, available_cash, CE_position_exists, False, CE_symbol, None, count_CE, count_PE, mktpxy)
                
                    elif mktpxy == "Sell":
                        if nse_power > 0.75:
                            if PE_position_exists:
                                print(f"    {PE_symbol} is there, let's {BRIGHT_YELLOW}skip{RESET}")
                            else:
                                print(f"    {PE_symbol} not there, let's Buy")
                                await process_orders(broker, available_cash, False, PE_position_exists, None, PE_symbol, count_CE, count_PE, mktpxy)
                        else:
                            print(f"nse_power:{nse_power} is not high enough,{BRIGHT_YELLOW}skip{RESET}ping")
                
                elif mktpredict == "FALL":
                    if mktpxy == "Buy":
                        if nse_power < 0.25:
                            if CE_position_exists:
                                print(f"    {CE_symbol} is there, let's {BRIGHT_YELLOW}skip{RESET}")
                            else:
                                print(f"    {CE_symbol} not there, let's Buy")
                                await process_orders(broker, available_cash, CE_position_exists, False, CE_symbol, None, count_CE, count_PE, mktpxy)
                        else:
                            print(f"nse_power:{nse_power} is not low enough, {BRIGHT_YELLOW}skip{RESET}ping")
                
                    elif mktpxy == "Sell":
                        if PE_position_exists:
                            print(f"    {PE_symbol} is there, let's {BRIGHT_YELLOW}skip{RESET}")
                        else:
                            print(f"    {PE_symbol} not there, let's Buy")
                            await process_orders(broker, available_cash, False, PE_position_exists, None, PE_symbol, count_CE, count_PE, mktpxy)

            except Exception as e:
                print(f"Error: {e}")
                logging.error(f"Error in main(): {e}")

    finally:
        # Reset sys.stdout to its default value
        pass
        # sys.stdout = sys.__stdout__

async def run_main():
    await main()

# Run the asynchronous function using asyncio.run()
def sync_main():
    asyncio.run(run_main())

sync_main()
