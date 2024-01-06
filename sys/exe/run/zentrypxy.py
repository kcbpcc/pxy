import os
import logging
from rich.console import Console
import yfinance as yf
from toolkit.logger import Logger
from toolkit.currency import round_to_paise
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

# Intervals
intervals = [5, 4, 3, 2, 1]

# Function to calculate the Heikin-Ashi candle colors for the last three closed candles (1-day interval)
def calculate_last_three_heikin_ashi_colors_day(symbol):
    try:
        data = yf.Ticker(symbol).history(period='5d', interval='1d')
        ha_close = (data['Open'] + data['High'] + data['Low'] + data['Close']) / 4
        ha_open = (data['Open'].shift(1) + data['Close'].shift(1)) / 2

        current_color = 'Bear' if ha_close.iloc[-1] < ha_open.iloc[-1] else 'Bull'
        last_closed_color = 'Bear' if ha_close.iloc[-2] < ha_open.iloc[-2] else 'Bull'
        second_closed_color = 'Bear' if ha_close.iloc[-3] < ha_open.iloc[-3] else 'Bull'

        return current_color, last_closed_color, second_closed_color
    except Exception as e:
        logging.error(f"Error calculating Heikin-Ashi colors for {symbol} (1-day): {str(e)}")
        raise

# Function to calculate the Heikin-Ashi candle colors for the last three closed candles (5-minute interval)
def calculate_last_three_heikin_ashi_colors_min(symbol):
    try:
        data = yf.Ticker(symbol).history(period='1d', interval='5m')
        ha_close = (data['Open'] + data['High'] + data['Low'] + data['Close']) / 4
        ha_open = (data['Open'].shift(1) + data['Close'].shift(1)) / 2

        current_color = 'Bear' if ha_close.iloc[-1] < ha_open.iloc[-1] else 'Bull'
        last_closed_color = 'Bear' if ha_close.iloc[-2] < ha_open.iloc[-2] else 'Bull'
        second_closed_color = 'Bear' if ha_close.iloc[-3] < ha_open.iloc[-3] else 'Bull'

        return current_color, last_closed_color, second_closed_color
    except Exception as e:
        logging.error(f"Error calculating Heikin-Ashi colors for {symbol} (5-minute): {str(e)}")
        raise

# Function to check SMBPXY for a symbol
def get_smbpxy_check(symbol):
    try:
        for interval in intervals:
            current_color_day, last_closed_color_day, second_closed_color_day = calculate_last_three_heikin_ashi_colors_day(symbol)
            current_color_min, last_closed_color_min, second_closed_color_min = calculate_last_three_heikin_ashi_colors_min(symbol)

            if (
                (current_color_day == 'Bear' and last_closed_color_day == 'Bull' and second_closed_color_day == 'Bull') and
                (current_color_min == 'Bear' and last_closed_color_min == 'Bull' and second_closed_color_min == 'Bull')
            ):
                action = 'Sell'
                status = transact(symbol)
                logging.info(f"Sell order placed for {symbol}")
                return f"Symbol: {symbol}, SMBPXY Check: {action}, {status}"

            elif (
                (current_color_day == 'Bull' and last_closed_color_day == 'Bear' and second_closed_color_day == 'Bear') and
                (current_color_min == 'Bull' and last_closed_color_min == 'Bear' and second_closed_color_min == 'Bear')
            ):
                action = 'Buy'
                status = transact(symbol)
                logging.info(f"Buy order placed for {symbol}")
                return f"Symbol: {symbol}, SMBPXY Check: {action}, {status}"

            else:
                action = 'NONE'

        return f"Symbol: {symbol}, SMBPXY Check: {action}, Status: No action"

    except Exception as e:
        console.print(f"[red]Error determining smbpxy check for {symbol}: {e}[/red]")
        return f"Symbol: {symbol}, SMBPXY Check: NONE, Status: Error determining smbpxy check"

def transact(symbol):
    try:
        def get_ltp():
            ltp = -1
            key = "NSE:" + symbol
            resp = broker.kite.ltp(key)
            if resp and isinstance(resp, dict):
                ltp = resp[key]['last_price']
            return ltp

        ltp = get_ltp()
        logging.info(f"ltp for {symbol} is {ltp}")
        if ltp <= 0:
            return symbol

        order_id = broker.order_place(
            tradingsymbol=symbol,
            exchange='NSE',
            transaction_type='BUY',
            quantity=int(float(symbol['calculated'])),
            order_type='LIMIT',
            product='CNC',
            variety='regular',
            price=round_to_paise(ltp, buybuff)
        )
        if order_id:
            logging.info(
                f"BUY {order_id} placed for {symbol} successfully")
            order_id = broker.order_place(
                tradingsymbol=symbol,
                exchange='NSE',
                transaction_type='SELL',
                quantity=int(float(symbol['calculated'])),
                order_type='LIMIT',
                product='CNC',
                variety='regular',
                price=calc_target(ltp, symbol['res_3'])
            )
            if order_id:
                logging.info(
                    f"SELL {order_id} placed for {symbol} successfully")
    except Exception as e:
        logging.error(f"{str(e)} while placing order")
        return symbol

# Assuming symbol_df is defined elsewhere in your code
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
