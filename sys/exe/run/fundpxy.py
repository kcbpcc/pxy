import sys
import traceback  # Add this import statement
from toolkit.logger import Logger
from login_get_kite import get_kite, remove_token
from cnstpxy import dir_path
from utcpxy import peak_time

peak = peak_time()

# Configure logging
logging = Logger(30, dir_path + "main.log")

def calculate_decision():
    logging = Logger(30, dir_path + "main.log")
    # Save the original sys.stdout
    original_stdout = sys.stdout
    
    try:
        # Redirect sys.stdout to 'output.txt'
        with open('output.txt', 'w') as file:
            sys.stdout = file
    
            try:
                broker = get_kite()
            except Exception as e:
                remove_token(dir_path)
                print(traceback.format_exc())
                logging.error(f"{str(e)} unable to get holdings")
                sys.exit(1)
    
    finally:
        # Reset sys.stdout to its original value
        sys.stdout = original_stdout

    try:
        try:
            response = broker.kite.margins()
            opening_balance = response["equity"]["available"]["opening_balance"]
            live_balance = response["equity"]["available"]["live_balance"]
            delivery = response["equity"]["utilised"]["delivery"]
            option_premium = response["equity"]["utilised"]["option_premium"]
            available_margin = opening_balance + live_balance + delivery + option_premium
            utilized_margin = response["equity"]["utilised"]["debits"]
            available_cash = live_balance
        except Exception as e:
            #print(f"An error occurred: {e}")
            available_cash = 0
            live_balance = 0  # Ensure live_balance is defined
        limit = 10000 if peak == 'PEAKEND' else 50000
        decision = "YES" if available_cash > limit else "NO"
        optdecision = "YES" if available_cash > 10000 else "NO"
        # Only return the decision, not available_cash
        return decision, optdecision, available_cash, live_balance, limit


    except Exception as e:
        remove_token(dir_path)
        logging.error(f"{str(e)} unable to get available cash")
        return "NO", "NO", 0, 0, 0
