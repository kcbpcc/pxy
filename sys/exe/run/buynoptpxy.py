import asyncio
import sys
import logging
from buycomnoptpxy import construct_symbols, count_positions_by_type, check_existing_positions, mktpredict
from login_get_kite import get_kite, remove_token
from cnstpxy import dir_path
from strikpxy import get_prices
from exprpxy import month_expiry_date
from fundpxy import calculate_decision
from mktpxy import get_market_check
from rsnprntpxy import process_orders
onemincandlesequance, mktpxy_nifty = get_market_check('^NSEI')
async def main_nifty():
    try:
        with open('output.txt', 'w') as file:
            sys.stdout = file

            try:
                broker = get_kite()
            except Exception as e:
                remove_token(dir_path)
                logging.error(f"{str(e)} unable to get holdings")
                sys.exit(1)
            finally:
                sys.stdout = sys.__stdout__

        try:
            decision, optdecision, available_cash, live_balance, limit = calculate_decision()
            count_CE, count_PE = count_positions_by_type(broker, 'NIFTY', 25)

            expiry_year, expiry_month, expiry_day = month_expiry_date()
            strike_price = get_prices()[1]

            CE_symbols = construct_symbols(expiry_year, expiry_month, expiry_day, 'CE', strike_price)
            PE_symbols = construct_symbols(expiry_year, expiry_month, expiry_day, 'PE', strike_price)

            CE_positions_exist = [check_existing_positions(broker, symbol, 25) for symbol in CE_symbols]
            PE_positions_exist = [check_existing_positions(broker, symbol, 25) for symbol in PE_symbols]

            if mktpredict == "SIDE":
                for symbol in CE_symbols[:1]:
                    if mktpxy_nifty == "Buy":
                        exists = check_existing_positions(broker, symbol, 25)
                        await process_orders(broker, available_cash, exists, False, symbol, None, count_CE, count_PE, mktpxy_nifty)
                for symbol in PE_symbols[:1]:
                    if mktpxy_nifty == "Sell":
                        await process_orders(broker, available_cash, False, check_existing_positions(broker, symbol, 25), None, symbol, count_CE, count_PE, mktpxy_nifty)

            elif mktpredict == "RISE":
                for symbol in CE_symbols[:1]:
                    if mktpxy_nifty == "Buy" and not check_existing_positions(broker, symbol, 25):
                        await process_orders(broker, available_cash, False, False, symbol, None, count_CE, count_PE, mktpxy_nifty)
                for symbol in PE_symbols[:1]:
                    if mktpxy_nifty == "Sell" and not check_existing_positions(broker, symbol, 25) and nse_power > 0.85:
                        await process_orders(broker, available_cash, False, False, None, symbol, count_CE, count_PE, mktpxy_nifty)

            elif mktpredict == "FALL":
                for symbol in CE_symbols[:1]:
                    if mktpxy_nifty == "Buy" and not check_existing_positions(broker, symbol, 25) and nse_power < 0.15:
                        await process_orders(broker, available_cash, False, False, symbol, None, count_CE, count_PE, mktpxy_nifty)
                for symbol in PE_symbols[:1]:
                    if mktpxy_nifty == "Sell" and not check_existing_positions(broker, symbol, 25):
                        await process_orders(broker, available_cash, False, False, None, symbol, count_CE, count_PE, mktpxy_nifty)

        except Exception as e:
            logging.error(f"Error in main_nifty(): {e}")

    except Exception as e:
        logging.error(f"Error in redirecting stdout: {e}")

if __name__ == "__main__":
    try:
        asyncio.run(main_nifty())
    except Exception as e:
        logging.error(f"Error in main execution: {e}")

