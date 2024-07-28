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

def construct_symbols(expiry_year, expiry_month, option_type, strike_price):
    if expiry_month < 10:
        expiry_month = f"0{expiry_month}"  # Ensure two-digit month format
    symbols = []
    if option_type == "CE":
        symbols.append(f"NIFTY{expiry_year}{expiry_month}{strike_price}CE")
        symbols.append(f"NIFTY{expiry_year}{expiry_month}{strike_price + 100}CE")
        symbols.append(f"NIFTY{expiry_year}{expiry_month}{strike_price + 200}CE")
    elif option_type == "PE":
        symbols.append(f"NIFTY{expiry_year}{expiry_month}{strike_price}PE")
        symbols.append(f"NIFTY{expiry_year}{expiry_month}{strike_price - 100}PE")
        symbols.append(f"NIFTY{expiry_year}{expiry_month}{strike_price - 200}PE")
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
                print("Broker object successfully obtained.")
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
        print(f"Decision: {decision}, OptDecision: {optdecision}, Available Cash: {available_cash}, Live Balance: {live_balance}, Limit: {limit}")

        count_CE, count_PE = count_positions_by_type(broker)
        PE_weight = count_PE - count_CE
        CE_weight = count_CE - count_PE
        weight = abs(count_PE - count_CE)
        print(f"CE Count: {count_CE}, PE Count: {count_PE}, PE Weight: {PE_weight}, CE Weight: {CE_weight}, Weight: {weight}")

        print(f"{BRIGHT_YELLOW}{count_PE:02}📉:PE positions💧N-{showhand}🔥CE positions:📈{count_CE:02}{RESET}")
        
        expiry_year, expiry_month, expiry_day = month_expiry_date()
        print(f"Expiry Date: {expiry_year}-{expiry_month}-{expiry_day}")

        strike_price = get_prices()[1]  # Assuming this returns the current strike price
        print(f"Current Strike Price: {strike_price}")

        CE_symbols = construct_symbols(expiry_year, expiry_month, expiry_day, 'CE', strike_price)
        PE_symbols = construct_symbols(expiry_year, expiry_month, expiry_day, 'PE', strike_price)
        print(f"CE Symbols: {CE_symbols}")
        print(f"PE Symbols: {PE_symbols}")

        CE_positions_exist = [check_existing_positions(broker, symbol) for symbol in CE_symbols]
        PE_positions_exist = [check_existing_positions(broker, symbol) for symbol in PE_symbols]
        print(f"CE Positions Exist: {CE_positions_exist}")
        print(f"PE Positions Exist: {PE_positions_exist}")

        print(f"Market Prediction: {mktpredict}")
        print(f"Market Position: {mktpxy}")

        if mktpredict == "SIDE":
            print("Market Prediction is SIDE.")
            for symbol in CE_symbols[:1]:  # Take only the first CE symbol
                if mktpxy == "Buy":
                    exists = check_existing_positions(broker, symbol)
                    print(f"Checking CE Symbol {symbol} - Exists: {exists}")
                    await process_orders(broker, available_cash, exists, False, symbol, None, count_CE, count_PE, mktpxy)
        
            for symbol, exists in zip(PE_symbols[:1], PE_positions_exist[:1]):  # Take only the first PE symbol
                if mktpxy == "Sell":
                    print(f"Checking PE Symbol {symbol} - Exists: {exists}")
                    await process_orders(broker, available_cash, False, exists, None, symbol, count_CE, count_PE, mktpxy)
        
        elif mktpredict == "RISE":
            print("Market Prediction is RISE.")
            for symbol, exists in zip(CE_symbols[:1], CE_positions_exist[:1]):  # Take only the first CE symbol
                if mktpxy == "Buy" and not exists:  # Check if there's no existing position
                    print(f"Checking CE Symbol {symbol} - Exists: {exists}")
                    await process_orders(broker, available_cash, exists, False, symbol, None, count_CE, count_PE, mktpxy)
        
            for symbol in PE_symbols[:1]:  # Take only the first PE symbol
                exists = check_existing_positions(broker, symbol)
                if mktpxy == "Sell" and not exists and nse_power > 0.85:  # Check NSE power condition
                    print(f"Checking PE Symbol {symbol} - Exists: {exists}, NSE Power: {nse_power}")
                    await process_orders(broker, available_cash, False, exists, None, symbol, count_CE, count_PE, mktpxy)
        
        elif mktpredict == "FALL":
            print("Market Prediction is FALL.")
            for symbol in CE_symbols[:1]:  # Take only the first CE symbol
                exists = check_existing_positions(broker, symbol)
                if mktpxy == "Buy" and not exists and nse_power < 0.15:  # Check NSE power condition
                    print(f"Checking CE Symbol {symbol} - Exists: {exists}, NSE Power: {nse_power}")
                    await process_orders(broker, available_cash, exists, False, symbol, None, count_CE, count_PE, mktpxy)
        
            for symbol, exists in zip(PE_symbols[:1], PE_positions_exist[:1]):  # Take only the first PE symbol
                if mktpxy == "Sell" and not exists:  # Check if there's no existing position
                    print(f"Checking PE Symbol {symbol} - Exists: {exists}")
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



