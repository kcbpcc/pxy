# funds.py
import sys
from toolkit.logger import Logger
from login_get_kite import get_kite, remove_token
from cnstpxy import dir_path

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
                broker = get_kite(api="bypass", sec_dir=dir_path)
            except Exception as e:
                remove_token(dir_path)
                print(traceback.format_exc())
                logging.error(f"{str(e)} unable to get holdings")
                sys.exit(1)
    
    finally:
        # Reset sys.stdout to its original value
        sys.stdout = original_stdout

    try:
        # Assuming kite is defined somewhere in the get_kite function
        # Use the 'margins' method to get margin data without specifying a segment
        response = broker.kite.margins()

        # Access the available cash from the response
        available_cash = response["equity"]["available"]["live_balance"]

        # Define 'YES' or 'NO' based on the available cash
        decision = "YES" if available_cash > 2500000 else "NO"

        # Print the decision
        status_emoji = "✅" if decision == "YES" else "❌" if decision == "NO" else "❓"
        print(f"Funds: {round(available_cash, 0)} | Decision is {decision} to BUY {status_emoji}")

        # Only return the decision, not available_cash
        return decision

    except Exception as e:
        remove_token(dir_path)
        logging.error(f"{str(e)} unable to get available cash")
        return "NO"  # Return 'NO' in case of an error
