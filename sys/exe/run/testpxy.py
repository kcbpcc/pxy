from toolkit.logger import Logger
from toolkit.currency import round_to_paise
from login_get_kite import get_kite
from fundpxy import calculate_decision
from mktpxy import get_market_check
import traceback
import sys
import os
import datetime
from cnstpxy import dir_path

logging = Logger(30, dir_path + "main.log")

black_file = os.path.join(dir_path, "blacklist.txt")

# Import the options string formatting and confirmation functions
from nftpxy import OPTIONS

def get_current_thursday():
    today = datetime.datetime.now()

    # If today is Thursday, use today's date
    if today.weekday() == 3:  # Monday is 0, Sunday is 6
        return today
    
    # Otherwise, calculate the date of the next Thursday
    days_until_thursday = (3 - today.weekday()) % 7
    next_thursday = today + datetime.timedelta(days=days_until_thursday)
    
    return next_thursday

def user_confirmation():
    user_input = input("Do you want to proceed with the options string and place the order? (y/n): ").lower()
    return user_input == 'y'

try:
    try:
        broker = get_kite(api="bypass", sec_dir=dir_path)
    except Exception as e:
        remove_token(os.path.abspath(os.path.join(dir_path, '..')))
        print(traceback.format_exc())
        logging.error(f"{str(e)} unable to get holdings")
        sys.exit(1)

    # Example usage for generating options string
    current_thursday = get_current_thursday()
    options_str = "NIFTY{Year}{Month}{THURSDAY_DATE}{OPTIONS}PE"
    
    # Format the placeholders
    year = current_thursday.strftime("%y")
    month = str(current_thursday.month) if current_thursday.month != 1 else "12"
    thursday_date = current_thursday.strftime("%d").zfill(2)
    formatted_str = options_str.replace("{Year}", year).replace("{Month}", month).replace("{THURSDAY_DATE}", thursday_date).replace("{OPTIONS}", str(OPTIONS))

    
    print("Generated Options String:", formatted_str)

    if user_confirmation():
        # Your logic to proceed with the generated options string
        print("You chose to proceed.")

        # Use the margins method to get account balance
        response = broker.kite.margins()

        # Access the available cash from the response
        available_cash = response["equity"]["available"]["live_balance"]

        if available_cash > 11:
            # Place the market order with your specified parameters
            order_id = broker.order_place(
                tradingsymbol=formatted_str,
                exchange='NSE',  # Replace with your specific exchange
                transaction_type='BUY',
                quantity=50,  # Replace with your specific quantity
                order_type='MARKET',
                product='MIS',
            )
            print(f"Market Order placed successfully. Order ID: {order_id}")
        else:
            print("Insufficient funds. Order not placed.")

    else:
        print("You chose not to proceed.")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Include any cleanup or finalization logic here
    pass

