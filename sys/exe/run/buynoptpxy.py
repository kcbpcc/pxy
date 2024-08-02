import traceback
import sys
import logging
import asyncio
from login_get_kite import get_kite, remove_token
from cnstpxy import dir_path
from strikpxy import get_prices
from datetime import datetime, timedelta
from ordoptpxy import place_order
from smapxy import check_index_status
from mktpxy import get_market_check
from exprpxy import month_expiry_date
from clorpxy import BRIGHT_YELLOW, RESET
from predictpxy import predict_market_sentiment
from bpredictpxy import predict_bnk_sentiment

# Constants
mktpredict = predict_market_sentiment()
bmktpredict = predict_bnk_sentiment()
nsma = check_index_status('^NSEI')
onemincandlesequance, mktpxy = get_market_check('^NSEI')
bnkmaxcount = 24
nftmaxcount = 24

def construct_symbols(expiry_year, expiry_month, option_type, strike_price):
    """
    Construct option symbols for CE and PE.
    """
    symbols = []
    if option_type == "CE":
        symbols = [f"NIFTY{expiry_year}{expiry_month}{strike_price + i * 100}CE" for i in range(3)]
    elif option_type == "PE":
        symbols = [f"NIFTY{expiry_year}{expiry_month}{strike_price - i * 100}PE" for i in range(3)]
    return symbols

def count_positions_by_type(broker):
    """
    Count the number of CE and PE positions for NIFTY.
    """
    positions_net = broker.kite.positions()['net']
    count_CE = sum(1 for p in positions_net if p['tradingsymbol'].endswith('CE') and abs(p['quantity']) >= 25)
    count_PE = sum(1 for p in positions_net if p['tradingsymbol'].endswith('PE') and abs(p['quantity']) >= 25)
    return count_CE, count_PE

def check_existing_positions(broker, symbol):
    """
    Check if a position already exists for a given symbol.
    """
    positions_net = broker.kite.positions()['net']
    return any(p['tradingsymbol'][-7:] == symbol[-7:] and abs(p['quantity']) >= 25 for p in positions_net)

async def main():
    try:
        with open('output.txt', 'w') as file:
            sys.stdout = file  # Redirect stdout to file
            try:
                broker = get_kite()
            except Exception as e:
                remove_token(dir_path)
                logging.error(f"Error initializing broker: {str(e)}")
                print(traceback.format_exc())
                sys.exit(1)
    finally:
        sys.stdout = sys.__stdout__  # Reset stdout

    try:
        from fundpxy import calculate_decision
        decision, optdecision, available_cash, live_balance, limit = calculate_decision()

        count_CE, count_PE = count_positions_by_type(broker)
        strike_price = get_prices()[1]  # Assuming this returns the current strike price
        expiry_year, expiry_month, _ = month_expiry_date()

        #print(f"{BRIGHT_YELLOW}{count_PE:02} 📉:PE ━━━━ {strike_price} | {showhand} ━━━━ CE:📈 {count_CE:02}{RESET}")
        print(f"{BRIGHT_YELLOW}{count_PE:02} 📉:PE ━━━━ {strike_price} ━━━━ CE:📈 {count_CE:02}{RESET}")


        CE_symbols = construct_symbols(expiry_year, expiry_month, 'CE', strike_price)
        PE_symbols = construct_symbols(expiry_year, expiry_month, 'PE', strike_price)

        CE_positions_exist = [check_existing_positions(broker, symbol) for symbol in CE_symbols]
        PE_positions_exist = [check_existing_positions(broker, symbol) for symbol in PE_symbols]

        await process_orders(broker, available_cash, CE_positions_exist, PE_positions_exist, CE_symbols, PE_symbols, count_CE, count_PE, mktpxy)
    except Exception as e:
        logging.error(f"Error in main(): {e}")
        print(f"Error: {e}")

async def process_orders(broker, available_cash, CE_positions_exist, PE_positions_exist, CE_symbols, PE_symbols, count_CE, count_PE, mktpxy):
    """
    Process orders based on market conditions and existing positions.
    """
    if available_cash <= 10000:
        log_insufficient_funds(available_cash)
        return

    # Handle CE orders
    for i, symbol in enumerate(CE_symbols):
        if mktpredict == "RISE" or (mktpredict == "SIDE" and i == 0):
            await handle_order(broker, CE_positions_exist[i], symbol, count_CE, 'CE', mktpxy)

    # Handle PE orders
    for i, symbol in enumerate(PE_symbols):
        if mktpredict == "FALL" or (mktpredict == "SIDE" and i == 0):
            await handle_order(broker, PE_positions_exist[i], symbol, count_PE, 'PE', mktpxy)

async def handle_order(broker, position_exists, symbol, count, order_type, mktpxy):
    """
    Handle individual order processing for CE or PE.
    """
    if not position_exists and (order_type == 'CE' and mktpxy == 'Buy') or (order_type == 'PE' and mktpxy == 'Sell'):
        quantity = determine_quantity(symbol, count, 'BANKNIFTY', 'NIFTY', bnkmaxcount, nftmaxcount)
        if quantity > 0:
            await execute_order(broker, symbol, quantity)
            print_order_reason(symbol, position_exists, count, 'Hold')
        else:
            print(f"Not placing as {symbol} Maxed")
    else:
        print_order_reason(symbol, position_exists, count, 'Hold')

def determine_quantity(symbol, count, banknifty_prefix, nifty_prefix, bnkmaxcount, nftmaxcount):
    """
    Determine the quantity of orders based on symbol and current counts.
    """
    if symbol.startswith(banknifty_prefix) and count < bnkmaxcount:
        return 15 if ((symbol.endswith("PE") and bmktpredict == "FALL") or (symbol.endswith("CE") and bmktpredict == "RISE")) else 15
    elif symbol.startswith(nifty_prefix) and count < nftmaxcount:
        return 25
    return 0

async def execute_order(broker, symbol, quantity):
    """
    Execute the order through the broker.
    """
    buy_order_placed, buy_order_id = await place_order(broker, symbol, 'BUY', 'NRML', quantity, 'MARKET')
    if buy_order_placed:
        await send_telegram_message(f"🛫🛫🛫 🌱🌱🌱 ENTRY order placed for {symbol} placed successfully.")
        print(f"{symbol:>22} successful")
    else:
        print(f"Failed to place BUY order for {symbol}")

def print_order_reason(symbol, position_exists, count, action):
    """
    Print the reason for holding or not placing an order.
    """
    reason = f"|{action}|{'🥚' if position_exists else '🧺'}|"
    reason += "MaxOut" if count >= (bnkmaxcount if symbol.startswith('BANKNIFTY') else nftmaxcount) else ""
    if reason:
        print(f"{symbol}: {reason: >{39 - len(symbol)}}")

def log_insufficient_funds(available_cash):
    """
    Log and print a message for insufficient funds.
    """
    print(f"\033[91mNo sufficient funds available Cash💰: {int(round(available_cash / 1000))}K\033[0m")

async def run_main():
    await main()

def sync_main():
    asyncio.run(run_main())

if __name__ == "__main__":
    sync_main()

