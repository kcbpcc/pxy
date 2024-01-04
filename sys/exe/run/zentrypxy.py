import warnings
import logging
import pandas as pd
import yfinance as yf
from rich.console import Console

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='your_log_file.log'
)

# Suppress yfinance warnings
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)

# Intervals
intervals = [5, 4, 3, 2, 1]

# Create a Console instance for rich print formatting
console = Console()

# Function to calculate the Heikin-Ashi candle colors for the last three closed candles (1-day interval)
def calculate_last_three_heikin_ashi_colors_day(symbol):
    data = yf.Ticker(symbol).history(period='5d', interval='1d')
    ha_close = (data['Open'] + data['High'] + data['Low'] + data['Close']) / 4
    ha_open = (data['Open'].shift(1) + data['Close'].shift(1)) / 2

    current_color = 'Bear' if ha_close.iloc[-1] < ha_open.iloc[-1] else 'Bull'
    last_closed_color = 'Bear' if ha_close.iloc[-2] < ha_open.iloc[-2] else 'Bull'
    second_closed_color = 'Bear' if ha_close.iloc[-3] < ha_open.iloc[-3] else 'Bull'

    return current_color, last_closed_color, second_closed_color

# Function to calculate the Heikin-Ashi candle colors for the last three closed candles (5-minute interval)
def calculate_last_three_heikin_ashi_colors_min(symbol):
    data = yf.Ticker(symbol).history(period='1d', interval='5m')
    ha_close = (data['Open'] + data['High'] + data['Low'] + data['Close']) / 4
    ha_open = (data['Open'].shift(1) + data['Close'].shift(1)) / 2

    current_color = 'Bear' if ha_close.iloc[-1] < ha_open.iloc[-1] else 'Bull'
    last_closed_color = 'Bear' if ha_close.iloc[-2] < ha_open.iloc[-2] else 'Bull'
    second_closed_color = 'Bear' if ha_close.iloc[-3] < ha_open.iloc[-3] else 'Bull'

    return current_color, last_closed_color, second_closed_color

def transact(symbol):
    try:
        ltp = -1

        def get_ltp(exchange):
            nonlocal ltp
            key = f"{exchange}:{symbol}"
            resp = yf.Ticker(symbol).info
            if 'last_price' in resp:
                ltp = resp['last_price']
            return ltp

        ltp_nse = get_ltp('NSE')
        logging.info(f"LTP for {symbol} on NSE is {ltp_nse}")

        if ltp_nse <= 0:
            ltp_bse = get_ltp('BSE')
            logging.info(f"LTP for {symbol} on BSE is {ltp_bse}")

            if ltp_bse > 0:
                ltp = ltp_bse
            else:
                console.print(f"Status: No LTP available for {symbol}")
                return f"Status: No LTP available for {symbol}"

        quantity = int(10000 / ltp)

        if quantity > 0:
            # Place your order logic here
            # For demonstration, print the order status
            logging.info(f"Order placed for {symbol}")
            return f"Status: Buy order placed for {symbol}"
        else:
            reason = f"Skipping {symbol}: Calculated quantity is not positive"
            logging.warning(f"Status: {reason}")
            return f"Status: {reason}"

    except Exception as e:
        logging.error(f"Error while placing order: {str(e)}")
        return f"Status: Error while placing order for {symbol}"

# Read symbols from the CSV file
csv_file_path = 'zlistpxy.csv'
symbol_df = pd.read_csv(csv_file_path)

# Process each symbol
for symbol_row in symbol_df.iloc[:, 0]:
    symbol_with_ns = f"{symbol_row}.NS"
    symbol_without_ns = symbol_row

    smbpxy_check_result = get_smbpxy_check(symbol_with_ns)

    # Print smbpxy_check result
    console.print(smbpxy_check_result)

    # Check if an order was placed and print the result
    if "Buy order placed" in smbpxy_check_result:
        console.print(f"[green]Order placed for {symbol_with_ns}[/green]")
    else:
        console.print(f"[yellow]No order placed for {symbol_with_ns}[/yellow]")




