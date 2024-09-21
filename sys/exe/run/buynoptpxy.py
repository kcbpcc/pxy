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
from cmbddfpxy import process_data

# Configure logging
logging.basicConfig(filename='error.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

import pandas as pd

def qty_positions_by_type(positions_net, CE_symbol, PE_symbol, positions_df):
    qty_CE = 0
    qty_PE = 0
    CE_PLPREC = 0
    PE_PLPREC = 0

    for position in positions_net:
        matching_row = positions_df[positions_df['tradingsymbol'] == position['tradingsymbol']]
        
        if not matching_row.empty:
            if position['tradingsymbol'] == CE_symbol:
                qty_CE += int(abs(position['quantity']) / 25)
                CE_PLPREC = matching_row['PL%'].values[0]
                
            elif position['tradingsymbol'] == PE_symbol:
                qty_PE += int(abs(position['quantity']) / 25)
                PE_PLPREC = matching_row['PL%'].values[0]

    return qty_CE, qty_PE, CE_PLPREC, PE_PLPREC

def count_positions_by_type(positions_net):
    count_CE = 0
    count_PE = 0
    for position in positions_net:
        if position['tradingsymbol'].startswith('NIFTY') and abs(position['quantity']) >= 25:
            if position['tradingsymbol'].endswith('CE'):
                count_CE += 1
            elif position['tradingsymbol'].endswith('PE'):
                count_PE += 1
    return count_CE, count_PE

def check_existing_positions(positions_net, symbol):
    for position in positions_net:
        if position['tradingsymbol'][-7:] == symbol[-7:] and abs(position['quantity']) >= 25:
            return True
    return False

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

async def main():
    try:
        with open('output.txt', 'w') as file:
            sys.stdout = file

            try:
                broker = get_kite()
                sys.stdout = sys.__stdout__
            except Exception as e:
                remove_token(dir_path)
                print(traceback.format_exc())
                logging.error(f"{str(e)} - Unable to get holdings")
                sys.exit(1)

            try:
                from fundpxy import calculate_decision
                decision, optdecision, available_cash, live_balance, limit = calculate_decision()

                combined_df = process_data()
                positions_net = combined_df.to_dict('records')

                count_CE, count_PE = count_positions_by_type(positions_net)
                PE_weight = count_PE - count_CE
                CE_weight = count_CE - count_PE
                weight = abs(count_PE - count_CE)
                strike_price = CE_Strike
                print(f"{BRIGHT_YELLOW}{count_PE:02} 📉:PE   ━━━━ {strike_price} | {showhand} ━━━━   CE:📈 {count_CE:02}{RESET}")

                expiry_year, expiry_month, expiry_day = month_expiry_date()

                CE_symbol = construct_symbol(expiry_year, expiry_month, expiry_day, 'CE')
                PE_symbol = construct_symbol(expiry_year, expiry_month, expiry_day, 'PE')

                CE_position_exists = check_existing_positions(positions_net, CE_symbol)
                PE_position_exists = check_existing_positions(positions_net, PE_symbol)

                qty_CE, qty_PE, CE_PLPREC, PE_PLPREC = qty_positions_by_type(positions_net, CE_symbol, PE_symbol, combined_df)

                print(f"{PE_symbol}  {(f'{qty_PE}x' if PE_position_exists else '')}{'🥚' if PE_position_exists else '🛒'}  {PE_PLPREC:6.2f}".rjust(41))
                print(f"{CE_symbol}  {(f'{qty_CE}x' if CE_position_exists else '')}{'🥚' if CE_position_exists else '🛒'}  {CE_PLPREC:6.2f}".rjust(41))

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
                        if nse_power > 0.70:
                            if PE_position_exists:
                                if (PE_PLPREC < -20 and qty_PE < 2) or (PE_PLPREC < -40 and qty_PE < 3) or (PE_PLPREC < -80 and qty_PE < 4):
                                    print(f"    {PE_symbol} is there,But {BRIGHT_RED}Re-Buy{RESET}")
                                    await place_order(broker, PE_symbol, 'BUY', 'NRML', 25, 'MARKET')
                                else:
                                    print(f"    {PE_symbol} is there, let's {BRIGHT_YELLOW}skip{RESET}")
                            else:
                                print(f"    {PE_symbol} not there, let's Buy")
                                await process_orders(broker, available_cash, False, PE_position_exists, None, PE_symbol, count_CE, count_PE, mktpxy)
                        else:
                            print(f"nse_power:{nse_power} is not high enough,{BRIGHT_YELLOW}skipping{RESET}")
                
                elif mktpredict == "FALL":
                    if mktpxy == "Buy":
                        if nse_power < 0.30:
                            if CE_position_exists:
                                if (CE_PLPREC < -20 and qty_CE < 2) or (CE_PLPREC < -40 and qty_CE < 3) or (CE_PLPREC < -80 and qty_CE < 4):
                                    print(f"    {CE_symbol} is there,But {BRIGHT_RED}Re-Buy{RESET}")
                                    await place_order(broker, CE_symbol, 'BUY', 'NRML', 25, 'MARKET')
                                else:
                                    print(f"    {CE_symbol} is there, let's {BRIGHT_YELLOW}skip{RESET}")
                            else:
                                print(f"    {CE_symbol} not there, let's Buy")
                                await process_orders(broker, available_cash, CE_position_exists, False, CE_symbol, None, count_CE, count_PE, mktpxy)
                        else:
                            print(f"nse_power:{nse_power} is not low enough,{BRIGHT_YELLOW}skipping{RESET}")
                
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
