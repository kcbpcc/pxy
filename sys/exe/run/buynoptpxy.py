from datetime import datetime, timedelta
import traceback
import sys
import logging
import telegram
import asyncio
from login_get_kite import get_kite, remove_token
from cnstpxy import dir_path
from mktpxy import get_market_check
from nftpxy import nse_action, nse_power, Day_Change, Open_Change
from strikpxy import get_prices
noptions, _, _, _ = get_prices()
from cyclepxy import cycle
from utcpxy import peak_time
from macdpxy import calculate_macd_signal
from smaftypxy import check_nifty_status
from mktrndpxy import get_market_status_for_symbol
nmktpxy = get_market_status_for_symbol("^NSEI")

onemincandlesequance, mktpxy = get_market_check()
peak = peak_time()
macd = calculate_macd_signal("^NSEI")
SMAfty = check_nifty_status()
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

    # Calculate days until the next Thursday
    days_until_this_thursday = (3 - current_date.weekday() + 7) % 7

    # If today is Thursday, return today's date
    if days_until_this_thursday == 0:
        return current_date.strftime("%y"), current_date.strftime("%m"), current_date.strftime("%d").zfill(2)

    # Calculate the date of this Thursday
    this_thursday = current_date + timedelta(days=days_until_this_thursday)

    # Check if this Thursday is the last Thursday of the month
    last_day_of_month = (this_thursday.replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)
    if this_thursday.month != (this_thursday + timedelta(days=7)).month:
        if this_thursday.day > last_day_of_month.day - 7:
            return this_thursday.strftime("%y"), this_thursday.strftime("%m"), this_thursday.strftime("%d").zfill(2)

    # Extract year, month, and day components
    expiry_year = this_thursday.strftime("%y")  # Represent year with two digits
    expiry_month = this_thursday.strftime("%m").upper()  # Represent month with uppercase
    expiry_day = this_thursday.strftime("%d").zfill(2)  # Ensure date is represented with 2 digits

    return expiry_year, expiry_month, expiry_day


def construct_symbol(expiry_year, expiry_month, expiry_day, option_type):
    if expiry_day is None:
        return f"NIFTY{expiry_year}{expiry_month}{noptions}{option_type}"
    else:
        return f"NIFTY{expiry_year}{expiry_month}{expiry_day}{noptions}{option_type}"



# Define function to check existing positions for the symbol
def check_existing_positions(broker, symbol):
    positions_response = broker.kite.positions()
    positions_net = positions_response['net']

    for position in positions_net:
        if position['tradingsymbol'] == symbol and position['quantity'] >= 40:
            return True  # Existing positions found

    return False

# Define function to place order for the symbol
async def place_order(broker, symbol):
    try:
        order_id = broker.order_place(
            tradingsymbol=symbol,
            quantity=50,
            exchange="NFO",
            transaction_type='BUY',
            order_type='MARKET',
            product='NRML'
        )

        print(f"{symbol} is ordered")
        message_text = f"Option Order {symbol} placed successfully."
        # Send the message to Telegram
        await send_telegram_message(message_text)
        return True  # Order successful
    except Exception as e:
        print(f"Error placing Option order for {symbol}: {e}")
        return False  # Order failed

# Main function to orchestrate the workflow
async def main():
    symbol = None  # Initialize symbol with a default value

    try:
        # Redirect sys.stdout to 'output.txt'
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
        # Reset sys.stdout to its original value
        sys.stdout = sys.__stdout__

    expiry_year, expiry_month, expiry_day = get_this_thursday()
    option_type = None  # Default value
    
    # Determine option type based on nmktpxy
    if nmktpxy == 'Sell'and smanifty != 'above':
        option_type = 'PE'  # Put Option
    else:
        # Handle the case where nmktpxy doesn't match any condition
        # You can raise an exception, set a default value, or handle it in another way
        print("NIFTY - nmktpxy:", nmktpxy, "smanifty:", smanifty)
        sys.exit(0)  # For example, exit the program with an error status
    
    # Construct the symbol based on the determined expiry and option type
    symbol = construct_symbol(expiry_year, expiry_month, expiry_day, option_type)

    if check_existing_positions(broker, symbol):
        print(f"{symbol} is already there")
    else:
        order_placed = await place_order(broker, symbol)
        if not order_placed:
            print("Order failed. Check error messages.")

# Define async function to run main function
async def run_main():
    await main()

# Run the main asynchronous function
asyncio.run(run_main())
