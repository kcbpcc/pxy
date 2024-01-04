import asyncio
import sys
import os
import logging
import telegram
import pandas as pd
from rich.console import Console
import yfinance as yf
from toolkit.logger import Logger
from toolkit.currency import round_to_paise
from toolkit.utilities import Utilities
from login_get_kite import get_kite
from cnstpxy import dir_path, fileutils, buybuff, max_target
from buypluspxy import Trendlyne
from fundpxy import calculate_decision
from mktpxy import get_market_check

# Constants
BLACK_FILE = os.path.join(dir_path, "blacklist.txt")
LOG_FILE = "your_log_file.log"
CSV_FILE_PATH = "zlistpxy.csv"

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename=LOG_FILE
)

# Initialize logging
logger = Logger(10)

# Initialize console for rich print formatting
console = Console()

# Initialize Kite API
try:
    sys.stdout = open('output.txt', 'w')
    broker = get_kite(api="bypass", sec_dir=dir_path)
except Exception as e:
    logging.error(f"Error initializing Kite API: {str(e)}")
    sys.exit(1)

# Call the calculate_decision function to get the decision
decision = calculate_decision()

# Function to place an order
def transact(symbol, remaining_cash):
    response = broker.kite.margins()
    available_cash = response["equity"]["available"]["live_balance"]

    # Define ltp before the try block
    ltp = -1

    try:
        def get_ltp(exchange):
            nonlocal ltp  # Use nonlocal to reference the outer ltp variable
            key = f"{exchange}:{symbol}"
            resp = broker.kite.ltp(key)
            if resp and isinstance(resp, dict):
                ltp = resp[key]['last_price']
            return ltp

        # Try getting LTP from NSE
        ltp_nse = get_ltp('NSE')
        logging.info(f"LTP for {symbol} on NSE is {ltp_nse}")

        # If LTP from NSE is not available or <= 0, try getting LTP from BSE
        if ltp_nse <= 0:
            ltp_bse = get_ltp('BSE')
            logging.info(f"LTP for {symbol} on BSE is {ltp_bse}")

            # If LTP from BSE is available, use it
            if ltp_bse > 0:
                ltp = ltp_bse
            else:
                # Neither NSE nor BSE LTP is available, return with remaining_cash
                return symbol, remaining_cash

        # Check if available cash is greater than 5116
        if available_cash > 10000:
            # Place the order on the exchange where LTP is available
            order_id = broker.order_place(
                tradingsymbol=symbol,
                exchange='NSE' if ltp_nse > 0 else 'BSE',
                transaction_type='BUY',
                quantity=1,
                order_type='LIMIT',
                product='CNC',
                variety='regular',
                price=round_to_paise(ltp, 0.2)
            )
            if order_id:
                logging.info(
                    f"BUY {order_id} placed for {symbol} successfully")
                # No need to calculate remaining available cash in this case

                try:
                    message_text = f"{ltp} \nhttps://www.tradingview.com/chart/?symbol={symbol}"

                    # Define the bot token and your Telegram username or ID
                    bot_token = '6603707685:AAFhWgPpliYjDqeBY24UyDipBbuBavcb4Bo'  # Replace with your actual bot token
                    user_id = '-4080532935'  # Replace with your Telegram user ID

                    # Function to send a message to Telegram
                    async def send_telegram_message(message_text):
                        bot = telegram.Bot(token=bot_token)
                        await bot.send_message(chat_id=user_id, text=message_text)

                    # Send the 'row' content as a message to Telegram immediately after printing the row
                    asyncio.run(send_telegram_message(message_text))

                except Exception as e:
                    # Handle the exception (e.g., log it) and continue with your code
                    print(f"Error sending message to Telegram: {e}")

                return symbol, remaining_cash

        else:
            logging.warning(
                f"Skipping {symbol}: Remaining Cash: {int(remaining_cash)}")
        return symbol, remaining_cash

    except Exception as e:
        logging.error(f"Error while placing order: {str(e)}")
        return symbol, remaining_cash

        print(f"Available Cash: {remaining_cash}")
    elif decision == "NO":
        # Perform actions for "NO"
        print("\033[91mNo Funds Available \033[0m")

# Read symbols from the CSV file
symbol_df = pd.read_csv(CSV_FILE_PATH)

# Process each symbol
for symbol_row in symbol_df.iloc[:, 0]:
    # Check SMBPXY and place order
    smbpxy_check_result = get_smbpxy_check(symbol_row + ".NS")

    # Print smbpxy_check result
    console.print(smbpxy_check_result)

    # Check if an order was placed
    if "Buy order placed" in smbpxy_check_result or "Sell order placed" in smbpxy_check_result:
        console.print(f"[green]Order placed for {symbol_row}[/green]")
    else:
        console.print(f"[yellow]No order placed for {symbol_row}[/yellow]")
