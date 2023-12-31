from toolkit.logger import Logger
from toolkit.currency import round_to_paise
from toolkit.utilities import Utilities
from login_get_kite import get_kite
from cnstpxy import dir_path, fileutils, buybuff, max_target
import pandas as pd
import traceback
import sys
from fundpxy import calculate_decision
from mktpxy import get_market_check
import asyncio
import logging
import telegram
import yfinance as yf

mktchk = get_market_check('^NSEI')
logging = Logger(10)

black_file = dir_path + "blacklist.txt"

try:
    sys.stdout = open('output.txt', 'w')
    broker = get_kite(api="bypass", sec_dir=dir_path)

except Exception as e:
    print(traceback.format_exc())
    sys.exit(1)

# Call the calculate_decision function to get the decision
decision = calculate_decision()

if decision == "YES":
    # Rest of the code remains unchanged

    def calc_target(ltp, perc):
        resistance = round_to_paise(ltp, perc)
        target = round_to_paise(ltp, max_target)
        return max(resistance, target)

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
            logging.info(
                f"LTP for {dct['tradingsymbol']} on NSE is {ltp_nse}")

            # If LTP from NSE is not available or <= 0, try getting LTP from BSE
            if ltp_nse <= 0:
                ltp_bse = get_ltp('BSE')
                logging.info(
                    f"LTP for {dct['tradingsymbol']} on BSE is {ltp_bse}")

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

    symbols_to_sell = []  # Replace this with the list obtained from the

import pandas as pd
import yfinance as yf
from nftpxy import nse_action
from mktpxy import get_market_check

def analyze_stock(symbol):
    try:
        # Append ".NS" to the symbol to specify the NSE exchange
        symbol_with_exchange = symbol + ".NS"

        # Download historical stock data for the last 2 days with a daily interval
        data = yf.download(symbol_with_exchange, period="7d", interval="1d")
        
        # Calculate Heikin-Ashi candles for daily data
        data['Close'] = data['Close']
        data['Open'] = data['Open']

        # Check if yesterday's candle is red and today's candle is green
        daybeforeyesterday_close = data['Close'].iloc[-3]
        daybeforeyesterday_open = data['Open'].iloc[-3]
        yesterday_close = data['Close'].iloc[-2]
        yesterday_open = data['Open'].iloc[-2]
        today_close = data['Close'].iloc[-1]
        today_open = data['Open'].iloc[-1]
        mktpxy = get_market_check(symbol_with_exchange)
        
        if (
            daybeforeyesterday_close < daybeforeyesterday_open
            and yesterday_close > yesterday_open
            and today_close > today_open
            and (nse_action == 'Bull' or nse_action == 'Bullish')
            and mktpxy == 'Buy'
        ):
            return 'Buy'
        elif (
            daybeforeyesterday_close > daybeforeyesterday_open
            and yesterday_close < yesterday_open
            and today_close < today_open
            and (nse_action == 'Bear' or nse_action == 'Bearish')
            and mktpxy == 'Sell'
        ):
            return 'Sell'
        else:
            return 'None'

    except Exception as e:
        print(f"Error during data download for {symbol}: {e}")
        return 'Error'

df_yxp500 = pd.read_csv('yxp500.csv')
    df_HPdf = pd.read_csv('fileHPdf.csv')

    # Use 'tradingsymbol' as the column name
    symbol_list_yxp500 = df_yxp500['tradingsymbol'].tolist()

    # Exclude symbols from fileHPdf.csv
    symbol_list_to_analyze = [symbol for symbol in symbol_list_yxp500 if symbol not in df_HPdf['tradingsymbol'].tolist()]

    # Initialize an empty list to store symbols to sell
    symbols_to_sell = []

    # Analyze each symbol
    for symbol in symbol_list_to_analyze:
        decision = analyze_stock(symbol, nse_action)  # Pass nse_action as an argument
        print(f"Decision for {symbol}: {decision}")

        # Check if the decision is 'Sell' and append the symbol to the list
        if decision == 'Sell':
            symbols_to_sell.append(symbol)

    # Print the list of symbols to sell
    print("Symbols to Sell:", symbols_to_sell)

elif decision == "NO":
    # Perform actions for "NO"
    print("\033[91mNo Funds Avalable \033[0m")


