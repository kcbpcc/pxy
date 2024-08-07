# order_management.py
import requests

def calculate_totals(combined_df):
    if not combined_df.empty:
        extras_df = combined_df[(combined_df['exchange'] == 'NFO') & (combined_df['sell_quantity'] > 0)].copy()
        total_opt_pnl = int(extras_df['unrealised'].sum()) + ((-1) * int(extras_df['PnL'].sum()))
    else:
        total_opt_pnl = 0
    return total_opt_pnl

def send_telegram_message(message, bot_token, user_usernames):
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

def place_order(tradingsymbol, quantity, transaction_type, order_type, product, broker, message, bot_token, user_usernames):
    try:
        order_id = broker.order_place(
            tradingsymbol=tradingsymbol,
            quantity=quantity,
            exchange='NFO',
            transaction_type=transaction_type,
            order_type=order_type,
            product=product
        )
        if order_id:  # Check if order_id is valid
            print(f"Order placed successfully. Order ID: {order_id}")
            send_telegram_message(message, bot_token, user_usernames)
            return order_id
        else:
            print("Order placement failed. No valid order ID returned.")
            return None
    except Exception as e:
        print(f"Error placing order: {e}")
        return None
