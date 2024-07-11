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
    
            try:
                response = broker.kite.margins()
                print(response)  # Print the response to the output file
                available_cash = response["equity"]["available"]["live_balance"]
                delivery_utilised = response["equity"]["utilised"]["delivery"]
                cash_for_delivery = available_cash - delivery_utilised
                print(f"Cash available for delivery: {cash_for_delivery}")
            except Exception as e:
                print(f"An error occurred: {e}")
                available_cash = 0
                cash_for_delivery = 0

    finally:
        # Reset sys.stdout to its original value
        sys.stdout = original_stdout

    try:
        # Print the information again to the console
        response = broker.kite.margins()
        available_cash = response["equity"]["available"]["live_balance"]
        delivery_utilised = response["equity"]["utilised"]["delivery"]
        cash_for_delivery = available_cash - delivery_utilised
        print(f"Response: {response}")
        print(f"Cash available for delivery: {cash_for_delivery}")

        limit = 50000 if peak == 'NONPEAK' else 10000 if peak == 'PEAKEND' else 0
        decision = "YES" if available_cash > limit else "NO"
        optdecision = "YES" if available_cash > 10000 else "NO"
        
        # Only return the decision, not available_cash
        return decision, optdecision, available_cash, limit

    except Exception as e:
        remove_token(dir_path)
        logging.error(f"{str(e)} unable to get available cash")
        return "NO", "NO", 0, 0

