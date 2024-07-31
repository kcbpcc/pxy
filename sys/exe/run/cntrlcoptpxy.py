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
from depthpxy import calculate_consecutive_candles
from mktpxy import get_market_check
from predictpxy import predict_market_sentiment
from bpredictpxy import predict_bnk_sentiment
from clorpxy import SILVER, UNDERLINE, RED, GREEN, YELLOW, RESET, BRIGHT_YELLOW, BRIGHT_RED, BRIGHT_GREEN, BOLD, GREY

# Common configurations
bot_token = 'YOUR_BOT_TOKEN'
user_usernames = ('YOUR_USER_ID',)

# Common functions
def initialize_broker():
    try:
        sys.stdout = open('output.txt', 'w')
        broker = get_kite()
        return broker
    except Exception as e:
        remove_token(dir_path)
        print(traceback.format_exc())
        logging.error(f"{str(e)} unable to get holdings")
        sys.exit(1)
    finally:
        if sys.stdout != sys.__stdout__:
            sys.stdout.close()
            sys.stdout = sys.__stdout__

def calculate_totals(combined_df):
    if not combined_df.empty:
        extras_df = combined_df[(combined_df['exchange'] == 'NFO') & (combined_df['sell_quantity'] > 0)].copy()
        total_opt_pnl = int(extras_df['unrealised'].sum()) + ((-1) * int(extras_df['PnL'].sum()))
    else:
        total_opt_pnl = 0
    return total_opt_pnl

def send_telegram_message(message):
    try:
        for username in user_usernames:
            url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
            payload = {'chat_id': username, 'text': message}
            response = requests.post(url, data=payload)
            if response.status_code != 200:
                print(f"Failed to send Telegram message. Status code: {response.status_code}")
            else:
                print("Telegram message sent successfully.")
    except Exception as e:
        print(f"Error sending Telegram message: {e}")

def place_order(broker, tradingsymbol, quantity, transaction_type, order_type, product):
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

def exit_options(exe_opt_df, broker):
    total_opt_pnl = calculate_totals(exe_opt_df)
    try:
        for _, row in exe_opt_df.iterrows():
            total_pl_percentage = row['PL%']
            tgtoptsmadepth = row['tgtoptsmadepth']
            
            if total_pl_percentage > tgtoptsmadepth and row['PnL'] > 400:
                place_order(broker, row['key'], row['qty'], 'SELL', 'MARKET', 'NRML')
                message = (
                    f"🛬🛬🛬 🎯🎯🎯 EXIT order placed {row['key']} successfully.\n"
                    f"🎯 Target PL%: {round(tgtoptsmadepth, 4)}%\n"
                    f"🏆 Reached PL%: {round(total_pl_percentage, 2)}%\n"
                    f"📉 Sell Price: {row['ltp']}\n"
                    f"📈 Buy Price: {row['avg']}\n"
                    f"💰 Booked Profit: {row['PnL']}\n"
                    f"Total Booked:💰 {total_opt_pnl} 📣"
                )
                print(message)
                send_telegram_message(message)
    except Exception as e:
        print(f"Error placing exit order: {e}")

def format_row(row, widths):
    symbol = row['tradingsymbol'][:int(widths['tradingsymbol'])].ljust(int(widths['tradingsymbol']))
    qty = f"{int(row['qty'])}".rjust(int(widths['qty']))
    pl_pct = f"{row['PL%']:.1f}".rjust(int(widths['PL%']))
    tgtoptsmadepth = f"{row['tgtoptsmadepth']:.1f}".rjust(int(widths['tgtoptsmadepth']))
    pnl = f"{int(row['PnL'])}".rjust(int(widths['PnL']))
    return f"{symbol}{qty}{pl_pct}{tgtoptsmadepth}{pnl}"

def prepare_data_and_apply_depth(symbol, df, sma, vix):
    df['key'] = df['key'].str.replace('NFO:', '')
    df['PL%'] = (df['PnL'] / df['Invested']) * 100
    df['PL%'] = df['PL%'].fillna(0)
    df['strike'] = df['key'].str.replace(r'(PE|CE)$', '', regex=True)

    def compute_tgtoptsma(row):
        if (sma == "up" and "CE" in row['key']) or (sma == "down" and "PE" in row['key']):
            return 7
        else:
            return 5

    df['tgtoptsma'] = df.apply(compute_tgtoptsma, axis=1)
    cedepth, pedepth = calculate_consecutive_candles(symbol)

    def compute_depth(row):
        try:
            if "CE" in row['key'] and cedepth > 1:
                return max(row['tgtoptsma'], (vix + 9 - cedepth))
            elif "PE" in row['key'] and pedepth > 1:
                return max(row['tgtoptsma'], (vix + 9 - pedepth))
            else:
                return 5
        except Exception as e:
            return 5

    df['tgtoptsmadepth'] = df.apply(compute_depth, axis=1)
    return df

