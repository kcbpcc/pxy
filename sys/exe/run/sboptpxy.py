
import traceback
import sys
import logging
import telegram
import asyncio
from login_get_kite import get_kite, remove_token
from cnstpxy import dir_path
from strikpxy import get_prices
from optpxy import get_opt_check
from macdpxy import calculate_macd_signal
from smapxy import check_index_status
from datetime import datetime, timedelta

# Initialize logging
logging.basicConfig(filename='output.log', level=logging.DEBUG)

async def send_telegram_message(message_text):
    try:
        bot_token = '6924826872:AAHTiMaXmjyYbGsCFhdZlRRXkyfZTpsKPug'
        user_usernames = '-4135910842'
        bot = telegram.Bot(token=bot_token)
        await bot.send_message(chat_id=user_usernames, text=message_text)
    except Exception as e:
        logging.error(f"Error sending message to Telegram: {e}")

def get_this_thursday():
    try:
        current_date = datetime.now()
        days_until_this_thursday = (3 - current_date.weekday() + 7) % 7
        if days_until_this_thursday == 0:
            return current_date.strftime("%y"), current_date.strftime("%m"), current_date.strftime("%d").zfill(2)
        this_thursday = current_date + timedelta(days=days_until_this_thursday)
        last_day_of_month = (this_thursday.replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)
        if this_thursday.month != (this_thursday + timedelta(days=7)).month:
            if this_thursday.day > last_day_of_month.day - 7:
                return this_thursday.strftime("%y"), this_thursday.strftime("%m"), this_thursday.strftime("%d").zfill(2)
        expiry_year = this_thursday.strftime("%y")
        month_number = int(this_thursday.strftime("%m"))
        expiry_month = str(month_number) if month_number <= 9 else this_thursday.strftime("%m")
        expiry_day = this_thursday.strftime("%d").zfill(2)
        return expiry_year, expiry_month, expiry_day
    except Exception as e:
        logging.error(f"Error getting this Thursday's date: {e}")

def construct_symbol(expiry_year, expiry_month, expiry_day, option_type, noptions):
    try:
        if len(expiry_month) == 2 and expiry_month.startswith("0"):
            expiry_month = expiry_month[1]
        if expiry_day is None:
            return f"NIFTY{expiry_year}{expiry_month}{noptions - 100}{option_type}"
        else:
            return f"NIFTY{expiry_year}{expiry_month}{expiry_day}{noptions - 100}{option_type}"
    except Exception as e:
        logging.error(f"Error constructing symbol: {e}")

def check_existing_positions(broker, symbol):
    try:
        positions_response = broker.kite.positions()
        positions_net = positions_response['net']
        for position in positions_net:
            if position['tradingsymbol'] == symbol and position['quantity'] < -300:
                return True
        return False
    except Exception as e:
        logging.error(f"Error checking existing positions: {e}")

async def place_order(broker, symbol, transaction_type, product_type, quantity, order_type, price=None):
    try:
        if price is None:
            order_id = broker.order_place(
                tradingsymbol=symbol,
                quantity=quantity,
                exchange="NFO",
                transaction_type=transaction_type,
                order_type=order_type,
                product=product_type
            )
        else:
            order_id = broker.order_place(
                tradingsymbol=symbol,
                quantity=quantity,
                exchange="NFO",
                transaction_type=transaction_type,
                order_type=order_type,
                product=product_type,
                price=price
            )
        return True, order_id
    except Exception as e:
        logging.error(f"Error placing order for {symbol}: {e}")
        return False, None

async def main():
    try:
        with open('output.txt', 'w') as file:
            sys.stdout = file
            try:
                broker = get_kite(api="bypass", sec_dir=dir_path)
            except Exception as e:
                remove_token(dir_path)
                logging.error(f"Error getting kite: {traceback.format_exc()}")
                logging.error(f"Error getting kite: {str(e)} unable to get holdings")
                sys.exit(1)
    finally:
        sys.stdout = sys.__stdout__
    
    try:
        expiry_year, expiry_month, expiry_day = get_this_thursday()
        ce_option_type = 'CE'
        pe_option_type = 'PE'
        
        ce_symbol = construct_symbol(expiry_year, expiry_month, expiry_day, ce_option_type, noptions)
        pe_symbol = construct_symbol(expiry_year, expiry_month, expiry_day, pe_option_type, noptions)
        
        total_funds_needed = await calculate_total_funds_needed(broker, ce_symbol, pe_symbol)
        
        decision = await get_funds_decision(broker, total_funds_needed)
        print("Funds Decision:", decision)
        
        if decision == "YES":
            print("Funds are sufficient for both CE and PE options.")
        else:
            print("Funds are not sufficient for both CE and PE options. Exiting.")
            return
        
        if check_existing_positions(broker, ce_symbol) or check_existing_positions(broker, pe_symbol):
            print(f"Existing order for {ce_symbol} or {pe_symbol} found. Skipping order placement.")
            return
        
        ce_sell_order_placed, ce_sell_order_id = await place_order(broker, ce_symbol, 'SELL', 'MIS', 50, 'MARKET')
        pe_sell_order_placed, pe_sell_order_id = await place_order(broker, pe_symbol, 'SELL', 'MIS', 50, 'MARKET')
        
        if ce_sell_order_placed and pe_sell_order_placed:
            print("SELL orders for CE and PE placed successfully.")
        else:
            print("Failed to place one or both SELL orders. Check logs for details.")
    except Exception as e:
        logging.error(f"Error in main: {e}")

async def calculate_total_funds_needed(broker, ce_symbol, pe_symbol):
    try:
        def get_ltp(symbol):
            ltp = [0]
            key = f"NFO:{symbol}"
            resp = broker.kite.ltp(key)
            if resp and isinstance(resp, dict):
                ltp[0] = resp[key]['last_price']
            return ltp[0]
        
        ltp_ce = get_ltp(ce_symbol)
        ltp_pe = get_ltp(pe_symbol)
        
        quantity = 50
        total_funds_needed = (ltp_ce + ltp_pe) * quantity * 2
        return total_funds_needed
    except Exception as e:
        logging.error(f"Error calculating total funds needed: {e}")
        return 0

# Run the main function
asyncio.run(main())
