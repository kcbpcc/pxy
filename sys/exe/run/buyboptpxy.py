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
from bftpxy import get_bnk_action
from predictpxy import predict_market_sentiment
from bpredictpxy import predict_bnk_sentiment
from clorpxy import SILVER, UNDERLINE, RED, GREEN, YELLOW, RESET, BRIGHT_YELLOW, BRIGHT_RED, BRIGHT_GREEN, BOLD, GREY
from hndmktpxy import hand
from nftpxy import ha_nse_action, nse_power, Day_Change, Open_Change

# Initialize variables
adjust = 0
BCE_Strike, _, _, BPE_Strike = get_prices()
#print(f"Strikes: BCE_Strike = {BCE_Strike}, BPE_Strike = {BPE_Strike}")

nsma = check_index_status('^NSEBANK')
#print(f"NSMA: {nsma}")

onemincandlesequance, mktpxy = get_market_check('^NSEBANK')
#print(f"Market Check: {onemincandlesequance}, {mktpxy}")

ha_nse_action, nse_power, Day_Change, Open_Change = get_bnk_action()
#print(f"Bank Action: ha_nse_action = {ha_nse_action}, nse_power = {nse_power}, Day_Change = {Day_Change}, Open_Change = {Open_Change}")

mktpredict = predict_market_sentiment()
#print(f"Market Sentiment Prediction: {mktpredict}")

bmktpredict = predict_bnk_sentiment()
#print(f"Bank Sentiment Prediction: {bmktpredict}")

showhand = hand(mktpxy)
#print(f"Show Hand: {showhand}")

def construct_symbol(expiry_year, expiry_month, expiry_day, option_type):
    # Convert expiry_month to a single digit string if it's less than or equal to 9
    if len(expiry_month) == 2 and expiry_month.startswith("0"):
        expiry_month = expiry_month[1]
    noptions = BPE_Strike if option_type == "PE" else (BCE_Strike if option_type == "CE" else None)
    if expiry_day is None:
        return f"BANKNIFTY{expiry_year}{expiry_month}{noptions}{option_type}"
    else:
        return f"BANKNIFTY{expiry_year}{expiry_month}{expiry_day}{noptions}{option_type}"

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
        # Redirect sys.stdout to 'output.txt'
        with open('output.txt', 'w') as file:
            sys.stdout = file

            try:
                broker = get_kite()
                #print("Broker login successful")
            except Exception as e:
                remove_token(dir_path)
                #print(traceback.format_exc())
                logging.error(f"{str(e)} unable to get holdings")
                sys.exit(1)

    finally:
        # Reset sys.stdout to its default value
        sys.stdout = sys.__stdout__

    try:
        from fundpxy import calculate_decision
        decision, optdecision, available_cash, live_balance, limit = calculate_decision()
        #print(f"Decision: {decision}, Opt Decision: {optdecision}, Available Cash: {available_cash}, Live Balance: {live_balance}, Limit: {limit}")

        count_CE, count_PE = count_positions_by_type(broker)
        #print(f"Position Counts: CE = {count_CE}, PE = {count_PE}")

        PE_weight = count_PE - count_CE
        CE_weight = count_CE - count_PE
        weight = abs(count_PE - count_CE)
        #print(f"Position Weights: PE_weight = {PE_weight}, CE_weight = {CE_weight}, Weight = {weight}")

        #print(f"{BRIGHT_YELLOW}{count_PE:02}📉:PE positions💧B-{showhand}🔥CE positions:📈{count_CE:02}{RESET}")

        expiry_year, expiry_month, expiry_day = month_expiry_date()
        #print(f"Expiry Date: Year = {expiry_year}, Month = {expiry_month}, Day = {expiry_day}")

        CE_symbol = construct_symbol(expiry_year, expiry_month, expiry_day, 'CE')
        PE_symbol = construct_symbol(expiry_year, expiry_month, expiry_day, 'PE')
        #print(f"Symbols: CE = {CE_symbol}, PE = {PE_symbol}")

        CE_position_exists = check_existing_positions(broker, CE_symbol)
        PE_position_exists = check_existing_positions(broker, PE_symbol)
        #print(f"Existing Positions: CE = {CE_position_exists}, PE = {PE_position_exists}")

        if bmktpredict == "SIDE":
            # Only place orders for symbols at the strike price
            #print("Market Predict: SIDE")
            #print(f"Placing SIDE order for CE: {CE_symbol}, Exists: {CE_position_exists}")
            if mktpxy == "Buy":
                await process_orders(broker, available_cash, CE_position_exists, False, CE_symbol, None, count_CE, count_PE, mktpxy)

            #print(f"Placing SIDE order for PE: {PE_symbol}, Exists: {PE_position_exists}")
            if mktpxy == "Sell":
                await process_orders(broker, available_cash, False, PE_position_exists, None, PE_symbol, count_CE, count_PE, mktpxy)

        elif bmktpredict == "RISE":
            #print("Market Predict: RISE")
            #print(f"Processing RISE order for CE: {CE_symbol}, Exists: {CE_position_exists}")
            if mktpxy == "Buy" and not CE_position_exists:
                await process_orders(broker, available_cash, CE_position_exists, False, CE_symbol, None, count_CE, count_PE, mktpxy)

            #print(f"Processing RISE order for PE: {PE_symbol}, Exists: {PE_position_exists}, NSE Power: {nse_power}")
            if mktpxy == "Sell" and not PE_position_exists and nse_power > 0.85:
                await process_orders(broker, available_cash, False, PE_position_exists, None, PE_symbol, count_CE, count_PE, mktpxy)

        elif bmktpredict == "FALL":
            #print("Market Predict: FALL")
            #print(f"Processing FALL order for CE: {CE_symbol}, Exists: {CE_position_exists}")
            if mktpxy == "Buy" and not CE_position_exists and nse_power < 0.15:
                await process_orders(broker, available_cash, CE_position_exists, False, CE_symbol, None, count_CE, count_PE, mktpxy)

            #print(f"Processing FALL order for PE: {PE_symbol}, Exists: {PE_position_exists}")
            if mktpxy == "Sell" and not PE_position_exists:
                await process_orders(broker, available_cash, False, PE_position_exists, None, PE_symbol, count_CE, count_PE, mktpxy)

    except Exception as e:
        #print(f"Error: {e}")
        logging.error(f"Error in main(): {e}")

async def run_main():
    await main()

# Run the asynchronous function using asyncio.run()
def sync_main():
    asyncio.run(run_main())

sync_main()


