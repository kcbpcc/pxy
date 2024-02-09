import traceback
import sys
import logging
import telegram
import asyncio
from login_get_kite import get_kite, remove_token
from nftpxy import OPTIONS
from cnstpxy import dir_path

# Store the original stdout
original_stdout = sys.stdout

# Define broker variable
broker = None

try:
    # Redirect sys.stdout to 'output.txt'
    with open('output.txt', 'w') as file:
        sys.stdout = file

        try:
            broker = get_kite(api="bypass", sec_dir=dir_path)
        except Exception as e:
            remove_token(dir_path)
            traceback.print_exc()
            logging.error(f"{str(e)} unable to get holdings")
            sys.exit(1)

finally:
    # Reset sys.stdout to its original value
    sys.stdout = original_stdout

# Define the function to send a message to Telegram
async def send_telegram_message(message_text):
    try:
        # Define the bot token and your Telegram username or ID
        bot_token = '6924826872:AAHTiMaXmjyYbGsCFhdZlRRXkyfZTpsKPug'  # Replace with your actual bot token
        user_usernames = ('-4135910842',)  # Replace with your Telegram username or ID

        # Create a Telegram bot
        bot = telegram.Bot(token=bot_token)

        # Send the message to Telegram
        await bot.send_message(chat_id=user_usernames, text=message_text)

    except Exception as e:
        # Handle the exception (e.g., log it) and continue with your code
        print(f"Error sending message to Telegram: {e}")

# Ensure that the 'broker' object has an 'order_place' method
if not broker or not hasattr(broker, 'order_place') or not callable(getattr(broker, 'order_place', None)):
    print("Error: 'broker' object is not properly initialized or does not have 'order_place' method.")
    sys.exit(1)

# Calculate the next Thursday date at least 6 days ahead
current_date = datetime.now()
days_until_next_thursday = (3 - current_date.weekday() + 7) % 7

# Ensure at least 6 days ahead
if days_until_next_thursday < 6:
    days_until_next_thursday += 7

next_thursday = current_date + timedelta(days=days_until_next_thursday)

# Format the date, month, and year
expiry_year = next_thursday.strftime("%y")
expiry_month = next_thursday.strftime("%m")
expiry_day = next_thursday.strftime("%d")

# Ensure the month is one digit until October
if int(expiry_month) < 10:
    expiry_month = expiry_month[1]

# Ensure the date is always two digits
expiry_day = expiry_day.zfill(2)

def get_ltp(exchange, symbol):
    try:
        key = f"{exchange}:{symbol}"
        resp = broker.kite.ltp([key])
        if resp and isinstance(resp, dict) and key in resp:
            return resp[key]['last_price']
    except Exception as e:
        print(f"Error getting LTP for {symbol}: {e}")
    return None

# Function to calculate funds needed for a given symbol and quantity
def calculate_funds_needed(exchange, symbol, quantity):
    ltp = get_ltp(exchange, symbol)
    if ltp is not None:
        return ltp * quantity
    else:
        return None

# Construct the symbol for the NIFTY Put Option
symbol_CE = f"NIFTY{expiry_year}{expiry_month}{expiry_day}{OPTIONS}CE"

# Place order directly
try:
    order_id_CE = broker.order_place(
        tradingsymbol=symbol_CE,
        quantity=50,
        exchange="NFO",
        transaction_type='BUY',
        order_type='MARKET',
        product='NRML'
    )

    print(f"{symbol_CE} Ordered") 
    message_text_CE = f"{symbol_CE} placed successfully"
    # Send the message to Telegram
    asyncio.run(send_telegram_message(message_text_CE))

except Exception as e:
    print("Error placing Call Option order:", e)
    order_id_CE = None  # Set order_id_CE to None to indicate failure

# Check if the order was successful
if order_id_CE is not None:
    print(f"{symbol_CE} Ordered") 
else:
    print("Order failed")
