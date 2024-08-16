import logging
from login_get_kite import get_kite
from cnstpxy import dir_path
from fundpxy import calculate_decision
from toolkit.currency import round_to_paise
import asyncio
import telegram
import yfinance as yf

# Hardcoded constants
BOT_TOKEN = '6924826872:AAHTiMaXmjyYbGsCFhdZlRRXkyfZTpsKPug'
USER_ID = '-4135910842'

# Set up logging
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

async def send_telegram_message(bot_token, user_id, message_text):
    bot = telegram.Bot(token=bot_token)
    await bot.send_message(chat_id=user_id, text=message_text)

def place_buy_order(random_symbol):
    try:
        # Fetch trading decision and available cash
        decision, optdecision, available_cash, live_balance, limit = calculate_decision()

        if decision != "YES":
            logger.info("Decision is not 'YES', skipping order placement.")
            return
        
        # Get broker instance
        broker = get_kite()

        # Get Last Traded Price (LTP)
        ltp_nse = broker.kite.ltp(f"NSE:{random_symbol}")[f"NSE:{random_symbol}"]['last_price']

        if ltp_nse >= 10000:
            logger.info(f"Skipping {random_symbol}: price is too high")
            return

        # Fetch current holdings, orders, and positions
        lst_dct_positions = broker.kite.positions()
        positions_symbols = [pos["tradingsymbol"] for pos in lst_dct_positions["day"] + lst_dct_positions["net"]]
        lst_dct_orders = broker.orders
        orders_symbols = [order.get("tradingsymbol", "Unknown Symbol") for order in lst_dct_orders]
        holdings = broker.kite.holdings()
        holdings_symbols = [holding["tradingsymbol"] for holding in holdings]

        # Determine purchase limit
        purchase_limit = 0
        if random_symbol in holdings_symbols and random_symbol not in orders_symbols and random_symbol not in positions_symbols:
            purchase_limit = 0
        elif random_symbol not in holdings_symbols and random_symbol not in orders_symbols and random_symbol not in positions_symbols:
            purchase_limit = 2000

        if purchase_limit <= 0:
            logger.info(f"Skipping {random_symbol}: purchase_limit is not set")
            return
        
        quantity = int(purchase_limit / ltp_nse)
        if quantity <= 0:
            logger.info(f"Skipping {random_symbol}: calculated quantity is zero or negative")
            return

        # Place order
        order_id = broker.order_place(
            tradingsymbol=random_symbol,
            exchange='NSE',
            transaction_type='BUY',
            quantity=quantity,
            order_type='LIMIT',
            product='CNC',
            variety='regular',
            price=round_to_paise(ltp_nse, 0.2)
        )

        if order_id:
            logger.info(f"BUY {order_id} placed for {random_symbol} successfully")
            remaining_cash = available_cash - (quantity * ltp_nse)
            print(f"Order placed successfully for {random_symbol}")
            print(f"Remaining Cash💰: {int(round(remaining_cash / 1000))}K")
            
            message_text = (f"📊 Let's Buy {random_symbol}!\n"
                            f"📈 Current Price (LTP): {ltp_nse}\n"
                            f"🔍 Check it out on TradingView: https://www.tradingview.com/chart/?symbol={random_symbol}")
            asyncio.run(send_telegram_message(BOT_TOKEN, USER_ID, message_text))
            
            if remaining_cash < limit:
                print(f"Cash: {int(remaining_cash)}, stopping further orders.")
                return
        else:
            logger.warning(f"Failed to place order for {random_symbol}")
    except Exception as e:
        logger.error(f"Error while placing order: {str(e)}")

