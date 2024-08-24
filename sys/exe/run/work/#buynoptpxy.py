from datetime import datetime, timedelta
import traceback
import sys
import logging
import telegram
import asyncio
from login_get_kite import get_kite, remove_token
from cnstpxy import dir_path
from strikpxy import get_prices
noptions, _, _, _ = get_prices()
from macdpxy import calculate_macd_signal
from mktrndpxy import get_market_status_for_symbol
nmktpxy = get_market_status_for_symbol("^NSEI")
from smaoptpxy import sma_above_or_below
smanifty = sma_above_or_below("^NSEI")
async def send_telegram_message(message_text):
    try:
        # Define the bot token and your Telegram username or ID
        bot_token = '6924826872:AAHTiMaXmjyYbGsCFhdZlRRXkyfZTpsKPug'  # Replace with your actual bot token
        user_usernames = '-4135910842'  # Replace with your Telegram username or ID
        # Create a Telegram bot
        bot = telegram.Bot(token=bot_token)
        # Send the message to Telegram
        await bot.send_message(chat_id=user_usernames, text=message_text)
    except Exception as e:
        # Handle the exception (e.g., log it) and continue with your code
        print(f"Error sending message to Telegram: {e}")
# Define function to get this week's Tuesday date
from datetime import datetime, timedelta
def get_this_thursday():
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

def construct_symbol(expiry_year, expiry_month, expiry_day, option_type):
    if expiry_day is None:
        return f"NIFTY{expiry_year}{expiry_month}{noptions}{option_type}"
    else:
        return f"NIFTY{expiry_year}{expiry_month}{expiry_day}{noptions}{option_type}"

def check_existing_positions(broker, symbol, transaction_type):
    positions_response = broker.kite.positions()
    positions_net = positions_response['net']
    for position in positions_net:
        # Check if 'tradingsymbol' matches and 'quantity' is at least 50
        if position['tradingsymbol'] == symbol and position['quantity'] >= 50:
            # If transaction_type is provided, check if it matches as well
            if 'transaction_type' in position and position['transaction_type'] == transaction_type:
                return True
            # If transaction_type is not provided, return True since tradingsymbol and quantity match
            elif not transaction_type:
                return True
    return False

async def place_order(broker, symbol, transaction_type, price=None):
    try:
        if transaction_type == 'BUY':
            order_id = broker.order_place(
                tradingsymbol=symbol,
                quantity=50,
                exchange="NFO",
                transaction_type=transaction_type,
                order_type='MARKET',
                product='NRML'
            )
        elif transaction_type == 'SELL':
            order_id = broker.order_place(
                tradingsymbol=symbol,
                quantity=50,
                exchange="NFO",
                transaction_type=transaction_type,
                order_type='SL',
                product='NRML',
                trigger_price=price  # Set the trigger price for stop-loss order
            )
        elif transaction_type == 'TARGET_SELL':
            order_id = broker.order_place(
                tradingsymbol=symbol,
                quantity=50,
                exchange="NFO",
                transaction_type='SELL',
                order_type='LIMIT',
                product='NRML',
                price=price  # Set the target sell price
            )
        message_text = f"Option Order {symbol} placed successfully."
        await send_telegram_message(message_text)
        return True, order_id
    except Exception as e:
        print(f"Error placing Option order for {symbol}: {e}")
        return False, None

async def get_ltp(broker, symbol):
    try:
        resp = broker.kite.ltp(symbol)
        if resp and isinstance(resp, dict):
            ltp = resp[symbol]['last_price']
            return ltp
        else:
            print("Invalid response or LTP not available.")
            return None
    except Exception as e:
        print(f"Error retrieving LTP for {symbol}: {e}")
        return None

async def main():
    symbol = None
    try:
        with open('output.txt', 'w') as file:
            sys.stdout = file
            try:
                broker = get_kite(api="bypass", sec_dir=dir_path)
            except Exception as e:
                remove_token(dir_path)
                traceback.format_exc()
                logging.error(f"{str(e)} unable to get holdings")
                sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
    finally:
        sys.stdout = sys.__stdout__
    expiry_year, expiry_month, expiry_day = get_this_thursday()
    option_type = None
    if nmktpxy == 'Sell' and smanifty != 'above':
        option_type = 'CE'  # Call Option
    elif smanifty != 'above':
        option_type = 'PE'  # Put Option
    else:
        option_type = 'PE'  # Put Option
        print("NIFTY - nmktpxy:", nmktpxy, "smanifty:", smanifty)
        sys.exit(0)
    symbol = construct_symbol(expiry_year, expiry_month, expiry_day, option_type)
    if check_existing_positions(broker, symbol, 'BUY'):
        print(f"Existing buy order for {symbol} found. Skipping buy order placement.")
    else:
        buy_order_placed, buy_order_id = await place_order(broker, symbol, 'BUY')
        if buy_order_placed:
            ltp = await get_ltp(broker, symbol)
            if ltp is not None:
                target_sell_price = ltp * 1.07  # 7% above
                if not check_existing_positions(broker, symbol, 'TARGET_SELL'):
                    target_sell_order_placed, _ = await place_order(broker, symbol, 'TARGET_SELL', target_sell_price)
                    if target_sell_order_placed:
                        print("Target sell order placed successfully.")
                        message_text = f"Target sell order for {symbol} placed successfully at {target_sell_price}."
                        await send_telegram_message(message_text)
                    else:
                        print("Target sell order placement failed.")
                        message_text = f"Failed to place target sell order for {symbol}."
                        await send_telegram_message(message_text)
                else:
                    print(f"Existing target sell order for {symbol} found. Skipping target sell order placement.")
            else:
                print("Failed to retrieve LTP. Unable to calculate target sell price.")
                message_text = "Failed to retrieve LTP. Unable to calculate target sell price."
                await send_telegram_message(message_text)
        else:
            print("Buy order placement failed.")
            message_text = f"Failed to place buy order for {symbol}."
            await send_telegram_message(message_text)

async def run_main():
    await main()

asyncio.run(run_main())
