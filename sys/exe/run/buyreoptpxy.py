import traceback
import sys
import asyncio
import telegram
import pandas as pd
from datetime import datetime, timedelta
from login_get_kite import get_kite, remove_token
from cnstpxy import dir_path

# Define a function to encapsulate the main logic
def execute_program(symbol):
    try:
        # Redirect sys.stdout to 'output.txt'
        with open('output.txt', 'w') as file:
            sys.stdout = file

            try:
                broker = get_kite(api="bypass", sec_dir=dir_path)
            except Exception as e:
                remove_token(dir_path)
                print(traceback.format_exc())
                print(f"Error: {str(e)} Unable to initialize Kite broker")
                sys.exit(1)

    finally:
        # Reset sys.stdout to its original value
        sys.stdout = sys.__stdout__

    # Define the function to send a message to Telegram
    async def send_telegram_message(message_text):
        try:
            # Define the bot token and your Telegram username or ID
            bot_token = 'YOUR_BOT_TOKEN'  # Replace with your actual bot token
            user_usernames = ['-4135910842']  # Replace with your Telegram username or ID

            # Create a Telegram bot
            bot = telegram.Bot(token=bot_token)

            # Send the message to Telegram
            await bot.send_message(chat_id=user_usernames[0], text=message_text)

        except Exception as e:
            # Handle the exception (e.g., log it) and continue with your code
            print(f"Error sending message to Telegram: {e}")

    # Read the CSV file to check if symbols exist
    try:
        df = pd.read_csv('fileHPdf.csv')
        existing_symbols = set(df['tradingsymbol'].tolist())
    except FileNotFoundError:
        existing_symbols = set()

    # Retrieve positions data
    try:
        positions_response = broker.kite.positions()
        positions_net = positions_response.get('net', [])
    except Exception as e:
        print(f"Error retrieving positions: {e}")
        positions_net = []

    # Create a list to store positions info
    positions_info = []
    
    # Store positions information in the list
    for position in positions_net:
        positions_info.append({
            'tradingsymbol': position.get('tradingsymbol', ''),
            'quantity': position.get('quantity', 0)
        })
    
    # Check if the symbol exists in the CSV file
    if symbol in existing_symbols:
        # Check if the quantity is greater than or equal to 50 in the CSV file
        quantity_in_csv = df.loc[df['tradingsymbol'] == symbol, 'quantity'].iloc[0]
        if quantity_in_csv >= 50:
            print(f"You already have 50 or more of {symbol}. Cannot buy more. Skipping order placement.")
            sys.exit(0)  # Exit the program
    
        # Check if the quantity is greater than 50 in the positions
        for position in positions_info:
            if position['tradingsymbol'] == symbol and position['quantity'] > 50:
                print(f"You already have more than 50 of {symbol}. Cannot buy more. Skipping order placement.")
                sys.exit(0)  # Exit the program

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
        expiry_month = expiry_month.zfill(2)

    # Ensure the date is always two digits
    expiry_day = expiry_day.zfill(2)

    # Extract strike price from the symbol if it contains one
    def extract_strike_price(symbol):
        for i in range(len(symbol)):
            if symbol[i:].isdigit():
                return symbol[i:]
        return None

    # Use the extracted strike price when constructing the symbol for the NIFTY Put Option
    strike_price = extract_strike_price(symbol)
    if strike_price:
        symbol_OPTIONS = f"NIFTY{expiry_year}{expiry_month}{expiry_day}{strike_price}CE"
    else:
        symbol_OPTIONS = f"NIFTY{expiry_year}{expiry_month}{expiry_day}CE"

    # Place order here
    try:
        order_id_OPTIONS = broker.order_place(
            tradingsymbol=symbol_OPTIONS,
            quantity=50,
            exchange="NFO",
            transaction_type='BUY',
            order_type='MARKET',
            product='NRML'
        )

        print(f"Ordered {symbol}")
        message_text_OPTIONS = f"REOPT - {symbol} placed successfully"
        # Send the message to Telegram
        asyncio.run(send_telegram_message(message_text_OPTIONS))

    except Exception as e:
        print("Error placing Call Option order:", e)
