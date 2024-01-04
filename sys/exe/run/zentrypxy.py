from toolkit.logger import Logger
from toolkit.currency import round_to_paise
from toolkit.utilities import Utilities
from login_get_kite import get_kite
from cnstpxy import dir_path, fileutils, buybuff, max_target
from buypluspxy import Trendlyne
import pandas as pd
import traceback
import sys
import os
from fundpxy import calculate_decision
from mktpxy import get_market_check
import asyncio
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

mktchk = get_market_check('^NSEI')
logging = Logger(10)
try:
    sys.stdout = open('output.txt', 'w')
    broker = get_kite(api="bypass", sec_dir=dir_path)

except Exception as e:
    print(traceback.format_exc())
    sys.exit(1)

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

def transact(dct, remaining_cash):
    response = broker.kite.margins()
    available_cash = response["equity"]["available"]["live_balance"]

    # Define ltp before the try block
    ltp = -1

    try:
        def get_ltp(exchange):
            nonlocal ltp  # Use nonlocal to reference the outer ltp variable
            key = f"{exchange}:{dct['tradingsymbol']}"
            resp = broker.kite.ltp(key)
            if resp and isinstance(resp, dict):
                ltp = resp[key]['last_price']
            return ltp

        # Try getting LTP from NSE
        ltp_nse = get_ltp('NSE')
        logging.info(f"LTP for {dct['tradingsymbol']} on NSE is {ltp_nse}")

        # If LTP from NSE is not available or <= 0, try getting LTP from BSE
        if ltp_nse <= 0:
            ltp_bse = get_ltp('BSE')
            logging.info(f"LTP for {dct['tradingsymbol']} on BSE is {ltp_bse}")

            # If LTP from BSE is available, use it
            if ltp_bse > 0:
                ltp = ltp_bse
            else:
                # Neither NSE nor BSE LTP is available, return with remaining_cash
                return dct['tradingsymbol'], remaining_cash

        # Check if available cash is greater than 5116
        if available_cash > 10000:
            # Place the order on the exchange where LTP is available
            order_id = broker.order_place(
                tradingsymbol=dct['tradingsymbol'],
                exchange='NSE' if ltp_nse > 0 else 'BSE',
                transaction_type='BUY',
                quantity=int(float(dct['QTY'].replace(',', ''))), 
                order_type='LIMIT',
                product='CNC',
                variety='regular',
                price=round_to_paise(ltp, 0.2)
            )
            if order_id:
                logging.info(
                    f"BUY {order_id} placed for {dct['tradingsymbol']} successfully")
                # No need to calculate remaining available cash in this case

                try:
                    message_text = f"{ltp} \nhttps://www.tradingview.com/chart/?symbol={dct['tradingsymbol']}"

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

                return dct['tradingsymbol'], remaining_cash

        else:
            logging.warning(
                f"Skipping {dct['tradingsymbol']}: Remaining Cash: {int(remaining_cash)}")
        return dct['tradingsymbol'], remaining_cash

    except Exception as e:
        logging.error(f"Error while placing order: {str(e)}")
        return dct['tradingsymbol'], remaining_cash

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

# Read symbols from the CSV file
csv_file_path = 'zlistpxy.csv'
symbol_df = pd.read_csv(csv_file_path)

# Process each symbol
for tradingsymbol in symbol_df.iloc[:, 0]:
    # Check SMBPXY and place order
    smbpxy_check_result = get_smbpxy_check(tradingsymbol+".NS")

    # Print smbpxy_check result
    console.print(smbpxy_check_result)

    # Check if an order was placed
    if "Buy order placed" in smbpxy_check_result or "Sell order placed" in smbpxy_check_result:
        console.print(f"[green]Order placed for {tradingsymbol}[/green]")
    else:
        console.print(f"[yellow]No order placed for {tradingsymbol}[/yellow]")


