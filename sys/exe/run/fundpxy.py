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
                
                # Calculate available and utilized margins
                available_margin = response["equity"]["available"]["live_balance"]
                utilized_margin = (
                    response["equity"]["utilised"]["debits"]
                    + response["equity"]["utilised"]["delivery"]
                    + response["equity"]["utilised"]["option_premium"]
                    + response["equity"]["utilised"]["payout"]
                    + response["equity"]["utilised"]["liquid_collateral"]
                    + response["equity"]["utilised"]["stock_collateral"]
                    + response["equity"]["utilised"]["span"]
                    + response["equity"]["utilised"]["exposure"]
                    + response["equity"]["utilised"]["additional"]
                    + response["equity"]["utilised"]["holding_sales"]
                    + response["equity"]["utilised"]["m2m_realised"]
                    + response["equity"]["utilised"]["m2m_unrealised"]
                )
                leftover_margin = available_margin - utilized_margin
                
                print(f"Available margin: {available_margin}")
                print(f"Utilized margin: {utilized_margin}")
                print(f"Leftover margin: {leftover_margin}")
            except Exception as e:
                print(f"An error occurred: {e}")
                available_margin = 0
                utilized_margin = 0
                leftover_margin = 0

    finally:
        # Reset sys.stdout to its original value
        sys.stdout = original_stdout

    try:
        # Print the information again to the console
        response = broker.kite.margins()
        available_margin = response["equity"]["available"]["live_balance"]
        utilized_margin = (
            response["equity"]["utilised"]["debits"]
            + response["equity"]["utilised"]["delivery"]
            + response["equity"]["utilised"]["option_premium"]
            + response["equity"]["utilised"]["payout"]
            + response["equity"]["utilised"]["liquid_collateral"]
            + response["equity"]["utilised"]["stock_collateral"]
            + response["equity"]["utilised"]["span"]
            + response["equity"]["utilised"]["exposure"]
            + response["equity"]["utilised"]["additional"]
            + response["equity"]["utilised"]["holding_sales"]
            + response["equity"]["utilised"]["m2m_realised"]
            + response["equity"]["utilised"]["m2m_unrealised"]
        )
        leftover_margin = available_margin - utilized_margin
        
        print(f"Response: {response}")
        print(f"Available margin: {available_margin}")
        print(f"Utilized margin: {utilized_margin}")
        print(f"Leftover margin: {leftover_margin}")

        limit = 50000 if peak == 'NONPEAK' else 10000 if peak == 'PEAKEND' else 0
        decision = "YES" if leftover_margin > limit else "NO"
        optdecision = "YES" if leftover_margin > 10000 else "NO"
        
        # Only return the decision, not available_margin
        return decision, optdecision, leftover_margin, limit

    except Exception as e:
        remove_token(dir_path)
        logging.error(f"{str(e)} unable to get available cash")
        return "NO", "NO", 0, 0
