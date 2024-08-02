import traceback
import sys
import logging
import asyncio
from datetime import datetime
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

# Initialize logging
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(message)s')

def get_cheapest_banknifty_symbol(expiry_year, expiry_month, expiry_day, option_type, kite):
    noptions = BPE_Strike if option_type == "PE" else (BCE_Strike if option_type == "CE" else None)
    
    if not noptions:
        logging.error("Invalid option type provided. Must be 'PE' or 'CE'.")
        return None, float('inf')
    
    symbol = f"BANKNIFTY{expiry_year}{expiry_month}{noptions}{option_type}"
    
    try:
        response = kite.ltp(f"NFO:{symbol}")
        ltp = response[f"NFO:{symbol}"]["last_price"]
        return symbol, ltp
    except Exception as e:
        logging.error(f"Error fetching price for {symbol}: {e}")
        return None, float('inf')

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
        # Redirect sys.stdout to 'output.txt' to suppress console output
        with open('output.txt', 'w') as file:
            sys.stdout = file

            try:
                broker = get_kite()
            except Exception as e:
                remove_token(dir_path)
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
            strike_price = BCE_Strike
            logging.info(f"{BRIGHT_YELLOW}{count_PE:02} 📉:PE   ━━━━ {strike_price} | {showhand} ━━━━   CE:📈 {count_CE:02}{RESET}")

            expiry_year, expiry_month, expiry_day = month_expiry_date()

            CE_symbol, CE_price = get_cheapest_banknifty_symbol(expiry_year, expiry_month, expiry_day, 'CE', broker)
            PE_symbol, PE_price = get_cheapest_banknifty_symbol(expiry_year, expiry_month, expiry_day, 'PE', broker)

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
            logging.error(f"Error in main(): {e}")

    except Exception as e:
        logging.error(f"Error in main(): {e}")

async def run_main():
    await main()

def sync_main():
    asyncio.run(run_main())

sync_main()

