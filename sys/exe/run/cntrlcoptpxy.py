import sys
import traceback
import pandas as pd
import requests
import logging
from login_get_kite import get_kite, remove_token
from cnstpxy import dir_path
from cmbddfpxy import process_data
from smapxy import check_index_status
from utcpxy import peak_time
from mktpxy import get_market_check
from predictpxy import predict_market_sentiment
from bpredictpxy import predict_bnk_sentiment
from clorpxy import SILVER, UNDERLINE, RED, GREEN, YELLOW, RESET, BRIGHT_YELLOW, BRIGHT_RED, BRIGHT_GREEN, BOLD, GREY

# Common configurations
bot_token = '7141714085:AAHlyEzszCy9N-L6wO1zSAkRwGdl0VTQCFI'
user_usernames = ('-4282665161',)

def get_vixpxy():
    # Placeholder values; replace with actual data fetching logic
    nifty_vix = 20.5
    bank_nifty_vix = 25.7
    return nifty_vix, bank_nifty_vix

def initialize_broker():
    try:
        return get_kite()
    except Exception as e:
        remove_token(dir_path)
        logging.error(f"{str(e)} unable to get holdings")
        print(traceback.format_exc())
        sys.exit(1)

def send_telegram_message(message):
    try:
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        for username in user_usernames:
            payload = {'chat_id': username, 'text': message}
            response = requests.post(url, data=payload)
            if response.status_code != 200:
                print(f"Failed to send Telegram message. Status code: {response.status_code}")
            else:
                print("Telegram message sent successfully.")
    except Exception as e:
        print(f"Error sending Telegram message: {e}")

def calculate_totals(combined_df):
    if not combined_df.empty:
        extras_df = combined_df[(combined_df['exchange'] == 'NFO') & (combined_df['sell_quantity'] > 0)].copy()
        total_opt_pnl = int(extras_df['unrealised'].sum()) + (-1 * int(extras_df['PnL'].sum()))
    else:
        total_opt_pnl = 0
    return total_opt_pnl

def format_row(row, widths):
    symbol = row['tradingsymbol'][:int(widths['tradingsymbol'])].ljust(int(widths['tradingsymbol']))
    qty = f"{int(row['qty'])}".rjust(int(widths['qty']))
    pl_pct = f"{row['PL%']:.1f}".rjust(int(widths['PL%']))
    tgtoptsmadepth = f"{row['tgtoptsmadepth']:.1f}".rjust(int(widths['tgtoptsmadepth']))
    pnl = f"{int(row['PnL'])}".rjust(int(widths['PnL']))
    return f"{symbol}{qty}{pl_pct}{tgtoptsmadepth}{pnl}"

def place_order(tradingsymbol, quantity, transaction_type, order_type, product, broker):
    try:
        order_id = broker.order_place(
            tradingsymbol=tradingsymbol,
            quantity=quantity,
            exchange='NFO',
            transaction_type=transaction_type,
            order_type=order_type,
            product=product
        )
        print(f"Order placed successfully. Order ID: {order_id}")
        return order_id
    except Exception as e:
        print(f"Error placing order: {e}")
        return None

def prepare_data_and_apply_depth(index_symbol, exe_opt_df, index_sma, vix):
    exe_opt_df['key'] = exe_opt_df['key'].str.replace('NFO:', '') 
    exe_opt_df['PL%'] = (exe_opt_df['PnL'] / exe_opt_df['Invested']) * 100
    exe_opt_df['PL%'] = exe_opt_df['PL%'].fillna(0)
    exe_opt_df['strike'] = exe_opt_df['key'].str.replace(r'(PE|CE)$', '', regex=True)
    exe_opt_df['tgtoptsma'] = exe_opt_df.apply(
        lambda row: 7 if (index_sma == "up" and "CE" in row['key']) or (index_sma == "down" and "PE" in row['key']) else 5, 
        axis=1
    )
    return exe_opt_df

