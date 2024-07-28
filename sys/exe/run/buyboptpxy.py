import asyncio
import sys
import logging
from buycomnoptpxy import construct_symbol, count_positions_by_type, check_existing_positions, mktpredict
from login_get_kite import get_kite, remove_token
from cnstpxy import dir_path
from strikpxy import get_prices
from exprpxy import month_expiry_date
from fundpxy import calculate_decision
from mktpxy import get_market_check
from rsnprntpxy import process_orders
from bpredictpxy import predict_bnk_sentiment
onemincandlesequance, mktpxy_bank = get_market_check('^NSEBANK')


async def main_bank():
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
            count_CE, count_PE = count_positions_by_type(broker, 'BANKNIFTY', 15)

            expiry_year, expiry_month, expiry_day = month_expiry_date()
            BCE_Strike, _, _, BPE_Strike = get_prices()
            CE_symbol = construct_symbol(expiry_year, expiry_month, expiry_day, 'CE', BCE_Strike)
            PE_symbol = construct_symbol(expiry_year, expiry_month, expiry_day, 'PE', BPE_Strike)

            CE_position_exists = check_existing_positions(broker, CE_symbol, 15)
            PE_position_exists = check_existing_positions(broker, PE_symbol, 15)

            bmktpredict = predict_bnk_sentiment()

            if bmktpredict == "SIDE":
                if mktpxy_bank == "Bull" and not CE_position_exists:
                    await process_orders(broker, available_cash, CE_position_exists, False, CE_symbol, None, count_CE, count_PE, mktpxy_bank)
                if mktpxy_bank == "Sell" and not PE_position_exists:
                    await process_orders(broker, available_cash, False, PE_position_exists, None, PE_symbol, count_CE, count_PE, mktpxy_bank)

            elif bmktpredict == "RISE":
                if mktpxy_bank == "Bull" and not CE_position_exists:
                    await process_orders(broker, available_cash, CE_position_exists, False, CE_symbol, None, count_CE, count_PE, mktpxy_bank)
                if mktpxy_bank == "Sell" and not PE_position_exists and nse_power > 0.85:
                    await process_orders(broker, available_cash, False, PE_position_exists, None, PE_symbol, count_CE, count_PE, mktpxy_bank)

            elif bmktpredict == "FALL":
                if mktpxy_bank == "Bull" and not CE_position_exists and nse_power < 0.15:
                    await process_orders(broker, available_cash, CE_position_exists, False, CE_symbol, None, count_CE, count_PE, mktpxy_bank)
                if mktpxy_bank == "Sell" and not PE_position_exists:
                    await process_orders(broker, available_cash, False, PE_position_exists, None, PE_symbol, count_CE, count_PE, mktpxy_bank)

        except Exception as e:
            logging.error(f"Error in main_bank(): {e}")

    except Exception as e:
        logging.error(f"Error in redirecting stdout: {e}")

if __name__ == "__main__":
    try:
        asyncio.run(main_bank())
    except Exception as e:
        logging.error(f"Error in main execution: {e}")



