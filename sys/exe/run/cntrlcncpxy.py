import os
import sys
import asyncio
import traceback
import telegram
import pandas as pd
import numpy as np
from tabulate import tabulate
from toolkit.logger import Logger
from toolkit.currency import round_to_paise
from login_get_kite import get_kite, remove_token
from cnstpxy import dir_path
from cmbddfpxy import process_data
from prftpxy import process_data_total_profit
from clorpxy import SILVER, UNDERLINE, RED, GREEN, YELLOW, RESET, BRIGHT_YELLOW, BRIGHT_RED, BRIGHT_GREEN, BOLD, GREY
from mktpxy import get_market_check
from nftpxy import get_nse_action
from predictpxy import predict_market_sentiment
from smapxy import check_index_status
from utcpxy import peak_time
from selfpxy import get_random_spiritual_message
from macdpxy import calculate_macd_signal
from fundpxy import calculate_decision


# Initialize logging
logging = Logger(30, os.path.join(dir_path, "main.log"))

# Setup
try:
    sys.stdout = open('output.txt', 'w')
    broker = get_kite()
except Exception as e:
    remove_token(dir_path)
    print(traceback.format_exc())
    logging.error(f"{str(e)}: unable to get holdings")
    sys.exit(1)

# Data processing
combined_df = process_data()
booked = process_data_total_profit()

def get_order_status(symbol, status_filter='ALL'):
    """Fetch order status based on the filter ('ALL' or 'OPEN')."""
    try:
        orders = broker.kite.orders()
        for order in orders:
            if status_filter == 'ALL' and order['tradingsymbol'] == symbol:
                return "YES"
            if status_filter == 'OPEN' and order['status'] == 'OPEN' and order['tradingsymbol'] == symbol:
                return "YES"
    except Exception as e:
        logging.error(f"Error fetching orders: {str(e)}")
        remove_token(dir_path)
        sys.exit(1)
    return "NO"

def place_sell_order(index, row):
    """Place a sell order and send a Telegram message."""
    try:
        exchsym = str(index).split(":")
        if len(exchsym) >= 2:
            logging.info(f"Placing order for {exchsym[1]}, {str(row)}")
            order_id = broker.order_place(
                tradingsymbol=exchsym[1],
                exchange=exchsym[0],
                transaction_type='SELL',
                quantity=int(row['qty']),
                order_type='LIMIT',
                product='CNC',
                variety='regular',
                price=round_to_paise(row['ltp'], -0.2)
            )
            if order_id:
                logging.info(f"Order {order_id} placed for {exchsym[1]} successfully")
                message_text = (
                    f"📊 Let's Book {exchsym[1]}!\n"
                    f"💰 Profit: {row['PnL']}\n"
                    f"💹 Profit %: {row['PL%']}\n"
                    f"🔢 H/P: {row['source']}\n"
                    f"📉 Sell Price: {row['ltp']}\n"
                    f"📈 Buy Price: {row['avg']}\n"
                    f"🔍 Check it out on TradingView: https://www.tradingview.com/chart/?symbol={exchsym[1]}\n"
                    f"Profits until: {booked} 📣"
                )
                asyncio.run(send_telegram_message(message_text))
                return True
            else:
                logging.error("Order placement failed")
        else:
            logging.error("Invalid format for 'index'")
    except Exception as e:
        logging.error(f"Error: {str(e)} while placing order")
    return False

def place_avg_order(index, row):
    """Place an average order and send a Telegram message."""
    try:
        exchsym = str(index).split(":")
        if len(exchsym) >= 2:
            positions_response = broker.kite.positions()
            open_positions = positions_response.get('net', [])
            existing_position = next((position for position in open_positions if position['tradingsymbol'] == exchsym[1]), None)
            if existing_position:
                logging.info(f"Position already exists for {exchsym[1]}. Skipping order placement.")
                return True

            qty = 1 if row['ltp'] > 1000 else 1000 // row['ltp']
            qty = int(qty)  # Remove decimals
            order_id = broker.order_place(
                tradingsymbol=exchsym[1],
                exchange=exchsym[0],
                transaction_type='BUY',
                quantity=qty,
                order_type='LIMIT',
                product='CNC',
                variety='regular',
                price=round_to_paise(row['ltp'], +0.3)
            )
            if order_id:
                logging.info(f"BUY {order_id} placed for {exchsym[1]} successfully")
                message_text = (
                    f"📊 Let's Average {exchsym[1]}!\n"
                    f"📈 Current Price (LTP): {row['ltp']}\n"
                    f"💰 Investment: {row['Invested']}\n"
                    f"📉 Avg: {row['avg']}\n"
                    f"🔍 Check it out on TradingView: https://www.tradingview.com/chart/?symbol={exchsym[1]}"
                )
                asyncio.run(send_telegram_message(message_text))
                return exchsym[1]
            return True
        else:
            logging.error("Order placement failed")
    except Exception as e:
        logging.error(f"Error: {str(e)} while placing order")
    return False

async def send_telegram_message(message_text):
    """Send a message via Telegram bot."""
    bot_token = 'YOUR_BOT_TOKEN_HERE'  # Replace with your actual bot token
    user_id = 'YOUR_USER_ID_HERE'  # Replace with your Telegram user ID
    bot = telegram.Bot(token=bot_token)
    await bot.send_message(chat_id=user_id, text=message_text)
###################################################################################"PXY® PreciseXceleratedYield Pvt Ltd™########################################################################################################################
# Get market data and other information
onemincandlesequance, mktpxy = get_market_check('^NSEI')
macd = calculate_macd_signal("^NSEI")
random_message = get_random_spiritual_message()
nsma = check_index_status('^NSEI')
peak = peak_time()

# Calculate decision
try:
    decision, optdecision, available_cash, live_balance, limit = calculate_decision()
except Exception as e:
    print(f"An error occurred: {e}")
    available_cash = 0

# Define a small constant
epsilon = 1e-10

# Function to calculate SMB power
def calculate_smb_power(row):
    start = row['low'] if row['source'] == 'holdings' else (row['avg'] if row['source'] == 'positions' else ValueError("Invalid value in 'source' column"))
    smb_power = round(abs(row['ltp'] - (start - 0.01)) / (abs(row['high'] + 0.01) - abs(start - 0.01) + epsilon), 2)
    return smb_power if abs(row['high'] + 0.01) - abs(start - 0.01) + epsilon != 0 and row['ltp'] - (start - 0.01) != 0 else 0.5

# Process combined DataFrame
combined_df['smb_power'] = combined_df.apply(calculate_smb_power, axis=1)
threshold = 3

# Predict market sentiment
mktpredict = predict_market_sentiment()
nsefactor = 6 if mktpredict == "RISE" else 0 if mktpredict == "FALL" else 3

# Calculate performance metrics
combined_df['fPL%'] = combined_df['smb_power'].apply(lambda x: round(np.exp(np.clip(((x + x) / 2), -threshold, threshold)), 2))
combined_df['tPL%'] = np.maximum(combined_df['fPL%'], np.maximum(1.4, np.round(np.exp(np.clip(((combined_df['fPL%'] + combined_df['fPL%']) / 2), -threshold, threshold)), 2)) * 1)
combined_df['tPL%'] = np.where(nsma == 'up', np.maximum(1 * (combined_df['tPL%'] * nse_power), 1.4), np.where(nsma == 'down', np.maximum((combined_df['tPL%'] * nse_power) * 0.5, 1.4), 1.4)) + 1.4 + nsefactor

# Round numeric columns
numeric_columns = ['fPL%','tPL%','smb_power','oPL%','qty', 'average_price', 'Invested','Yvalue', 'ltp','close', 'open', 'high', 'low','value', 'PnL', 'PL%', 'dPnL', 'dPL%']
combined_df[numeric_columns] = combined_df[numeric_columns].round(2)

# Filter and process DataFrames
total_opt_real = combined_df[(combined_df['qty'] == 0) & (combined_df['key'].str.contains('NFO:'))]['pnl'].sum()
filtered_df = combined_df[(combined_df['product'] == 'CNC') & (combined_df['qty'] != 0)]
pxy_df = filtered_df.copy()[['tPL%','fPL%','oPL%','dPL%','PnL', 'PL%','smb_power','Invested','source','product', 'qty','avg','ltp', 'open', 'high', 'close', 'low','key']]
pxy_df['avg'] = filtered_df['average_price']

EXE_df = pxy_df[['tPL%','fPL%','smb_power','oPL%','Invested','qty', 'avg', 'close', 'ltp', 'open', 'high', 'low', 'dPL%','product', 'source', 'key', 'PL%', 'PnL']]
PRINT_df = pxy_df[(pxy_df['qty'] > 0) & (~pxy_df['key'].str.contains('NFO'))][['source', 'key', 'dPL%', 'oPL%', 'tPL%', 'smb_power', 'PL%', 'PnL']]
PRINT_df = PRINT_df.rename(columns={'source': 'HP', 'smb_power': 'TR'})
PRINT_df['HP'] = PRINT_df['HP'].replace({'holdings': '📌', 'positions': '🎯'})
PRINT_df['TR'] = PRINT_df['TR'].apply(lambda TR: '⚪' if TR > 0.8 else ('🟢' if 0.5 < TR <= 0.8 else ('🟠' if 0.3 < TR <= 0.5 else ('🔴' if TR <= 0.3 else TR))))
PRINT_df['key'] = PRINT_df['key'].str.replace(r'BSE:|NSE:', '', regex=True)

# Sort and display the DataFrame
PRINT_df_sorted = PRINT_df.copy()
PRINT_df_sorted['TR'] = PRINT_df_sorted['TR'].apply(lambda TR: TR[:2] if isinstance(TR, str) else TR)
PRINT_df_sorted['key'] = PRINT_df_sorted['key'].str.replace(r'(BSE:|NSE:|NFO:)', '', regex=True).str[:7].str.ljust(7, ' ')
PRINT_df_sorted = PRINT_df_sorted.sort_values(by='PL%', ascending=True)
pd.set_option('display.max_colwidth', 1)
PRINT_df_sorted_display = PRINT_df_sorted.copy()
stocks_filtered_df = PRINT_df_sorted_display[PRINT_df_sorted_display['PL%'] > 1.4].sort_values(by='PL%')

# Handle stocks excluded from orders
if not os.path.exists("pxyexclude.csv"):
    df = pd.DataFrame(columns=["STOCK"])
    df.to_csv("pxyexclude.csv", index=False)
else:
    df = pd.read_csv("pxyexclude.csv")

selected_rows = []
try:
    for index, row in EXE_df.iterrows():
        excluded_keys = set(df['STOCK'])
        key = row['key']
        symbol_in_order = key.split(":")[1]

        if (
            symbol_in_order not in excluded_keys and
            row['open'] > 0 and
            row['high'] > 0 and
            row['low'] > 0 and
            row['close'] > 0 and
            nse_power != 0.50 and
            row['ltp'] != 0
        ):
            if (
                row['qty'] > 0 and
                row['avg'] != 0 and
                row['product'] == 'CNC' and
                row['PL%'] > 1.4 and 
                (mktpxy == "Sell" or mktpxy == "Bear") and
                (
                    (row['PL%'] > row['tPL%'] and row['PnL'] > 200) or 
                    (row['dPL%'] < 0 and row['oPL%'] < 0 and row['source'] == 'holdings' and mktpredict == "FALL") or
                    (row['PL%'] > 5 and row['PnL'] > 200 and row['source'] == 'positions')
                )
            ):
                try:
                    print(f"Trying to close: {row['key']}")
                    is_placed = stocks_sell_order_place(key, row) if get_open_order_status(symbol_in_order) == "NO" else False
                    if is_placed:
                        print(row)  # Optionally print the row after placing the order
                except Exception as e:
                    print(f"An unexpected error occurred while placing an order for key {key}: {e}")

            elif (
                row['qty'] > 0 and
                row['avg'] != 0 and
                row['Invested'] < 30000 and
                peak == 'PEAKEND' and
                available_cash > 1000 and
                row['dPL%'] < -1.4
            ):
                try:
                    # Read the stock symbols from stocks.csv
                    stocks_df = pd.read_csv('avgstocks')
                    stock_symbols = stocks_df['Symbol'].tolist()  # Assuming 'Symbol' is the column name in stocks.csv
                
                    # Define the order placement function
                    def place_order(symbol):
                        if get_open_order_status(symbol) == "NO":
                            is_placed = stocks_buy_order_place(symbol, row)
                            if is_placed:
                                print(f"Order placed for: {symbol}")
                            else:
                                print(f"Failed to place order for: {symbol}")
                        else:
                            print(f"Order already open for: {symbol}")

                    # Place orders for the first three available symbols
                    for symbol in stock_symbols[:3]:
                        place_order(symbol)
                except Exception as e:
                    print(f"An unexpected error occurred while placing an order: {e}")

except Exception as e:
    print(f"An error occurred: {e}")

# Display filtered and sorted DataFrame
print(tabulate(stocks_filtered_df, headers='keys', tablefmt='psql', showindex=False))
