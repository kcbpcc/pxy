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
from clorpxy import SILVER, UNDERLINE, RED, GREEN, YELLOW, RESET, BRIGHT_YELLOW, BRIGHT_RED, BRIGHT_GREEN, BOLD, GREY
from predictpxy import predict_market_sentiment

# Initialize constants
mktpredict = predict_market_sentiment()
nsma = check_index_status('^NSEI')
onemincandlesequance, mktpxy = get_market_check('^NSEI')
showhand = hand(mktpxy)

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

        expiry_year, expiry_month, expiry_day = month_expiry_date()
        strike_price = get_prices()[1]  # Assuming this returns the current strike price
        print(f"{BRIGHT_YELLOW}{count_PE:02} 📉:PE   ━━━━━ {strike_price} {showhand} ━━━━━   CE:📈 {count_CE:02}{RESET}")

        CE_symbols = construct_symbols(expiry_year, expiry_month, expiry_day, 'CE', strike_price)
        PE_symbols = construct_symbols(expiry_year, expiry_month, expiry_day, 'PE', strike_price)

        CE_positions_exist = [check_existing_positions(broker, symbol) for symbol in CE_symbols]
        PE_positions_exist = [check_existing_positions(broker, symbol) for symbol in PE_symbols]
        
        if mktpredict == "SIDE":
            # Only place orders for symbols at the strike price
            for symbol in CE_symbols[:1]:  # Take only the first CE symbol
                if mktpxy == "Buy":
                    exists = check_existing_positions(broker, symbol)
                    await process_orders(broker, available_cash, exists, False, symbol, None, count_CE, count_PE, mktpxy)
            
            for symbol in PE_symbols[:1]:  # Take only the first PE symbol
                if mktpxy == "Sell":
                    exists = check_existing_positions(broker, symbol)
                    await process_orders(broker, available_cash, False, exists, None, symbol, count_CE, count_PE, mktpxy)
        
        elif mktpredict == "RISE":
            for symbol, exists in zip(CE_symbols[:3], CE_positions_exist[:3]):  # Take the first three CE symbols
                if mktpxy == "Buy" and not exists:  # Check if there's no existing position
                    await process_orders(broker, available_cash, exists, False, symbol, None, count_CE, count_PE, mktpxy)
            
            for symbol in PE_symbols[:1]:  # Take only the first PE symbol
                exists = check_existing_positions(broker, symbol)
                if mktpxy == "Sell" and not exists and nse_power > 0.85:  # Check NSE power condition
                    await process_orders(broker, available_cash, False, exists, None, symbol, count_CE, count_PE, mktpxy)
        
        elif mktpredict == "FALL":
            for symbol in CE_symbols[:1]:  # Take only the first CE symbol
                exists = check_existing_positions(broker, symbol)
                if mktpxy == "Buy" and not exists and nse_power < 0.15:  # Check NSE power condition
                    await process_orders(broker, available_cash, exists, False, symbol, None, count_CE, count_PE, mktpxy)
            
            for symbol, exists in zip(PE_symbols[:3], PE_positions_exist[:3]):  # Take the first three PE symbols
                if mktpxy == "Sell" and not exists:  # Check if there's no existing position
                    await process_orders(broker, available_cash, False, exists, None, symbol, count_CE, count_PE, mktpxy)


    except Exception as e:
        print(f"Error: {e}")
        logging.error(f"Error in main(): {e}")

async def run_main():
    await main()

def sync_main():
    asyncio.run(run_main())

if __name__ == '__main__':
    sync_main()
