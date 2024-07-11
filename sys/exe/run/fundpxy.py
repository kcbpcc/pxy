import sys
import traceback
from toolkit.logger import Logger
from login_get_kite import get_kite, remove_token
from cnstpxy import dir_path
from utcpxy import peak_time

peak = peak_time()

# Configure logging
logging = Logger(30, dir_path + "main.log")

def calculate_decision():
    original_stdout = sys.stdout  # Save the original sys.stdout
    
    try:
        with open('output.txt', 'w') as file:
            sys.stdout = file  # Redirect sys.stdout to 'output.txt'
    
            try:
                broker = get_kite()
            except Exception as e:
                remove_token(dir_path)
                print(traceback.format_exc())
                logging.error(f"{str(e)}: unable to get holdings")
                sys.exit(1)
    
    finally:
        sys.stdout = original_stdout  # Reset sys.stdout to its original value

    try:
        # Assuming broker.kite is defined somewhere in the get_kite function
        try:
            response = broker.kite.margins()
            #total_cash_with_margin = response["equity"]["available"]["live_balance"]
            #used_margin = response["equity"]["utilised"]["debits"]
            #available_cash = total_cash_with_margin - used_margin

            total_balance = response["available"]["live_balance"]
            used_margin = response["utilised"]["debits"]
            available_cash = total_balance - used_margin



        
            # print(f"I have 💰💰💰💰{total_cash_with_margin/1000:.0f}K💰💰💰 to buy stocks")
        except Exception as e:
            print(f"An error occurred: {e}")
            logging.error(f"{str(e)}: unable to get margins")
            total_cash_with_margin = 0
            available_cash = 0
        
        limit = 25000 if peak == 'NONPEAK' else 10000 if peak == 'PEAKEND' else 0
        decision = "YES" if available_cash > limit else "NO"
        optdecision = "YES" if available_cash > 10000 else "NO"
        
        return decision, optdecision, available_cash, limit

    except Exception as e:
        remove_token(dir_path)
        logging.error(f"{str(e)}: unable to get available cash")
        return "NO", "NO", 0, 0


