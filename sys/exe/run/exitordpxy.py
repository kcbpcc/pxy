# order_handler.py
import logging
import csv
import telegram
import asyncio

def order_place(index, row, broker, csv_file_path, key, result):
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
                price=round_to_paise(row['ltp'], -0.3)
            )
            if order_id:
                logging.info(f"Order {order_id} placed for {exchsym[1]} successfully")
                # Write the row to the CSV file here
                with open(csv_file_path, 'a', newline='') as csvfile:
                    csvwriter = csv.writer(csvfile)
                    csvwriter.writerow(row.tolist())  # Write the selected row to the CSV file
                    try:
                        columns_to_drop = ['smb_power', 'oPL%', 'pstp', '_pstp', 'qty', 'close', 'open', 'high', 'low', 'PL%_H', 'dPL%', 'pxy','yxp']
                        # Dropping specified columns from the row
                        for column in columns_to_drop:
                            if column in row:
                                del row[column]

                        message_text = f"{str(row):>10} \nhttps://www.tradingview.com/chart/?symbol={key}\nBooked profit until now: {result}"

                        # Define the bot token and your Telegram username or ID
                        bot_token = '6409002088:AAH9mu0lfjvHl_IgRAgX7YrjJQa2Ew9qaLo'  # Replace with your actual bot token
                        user_usernames = ('-4022487175',)  # Replace with your Telegram username or ID

                        # Function to send a message to Telegram
                        async def send_telegram_message(message_text):
                            bot = telegram.Bot(token=bot_token)
                            await bot.send_message(chat_id=user_usernames, text=message_text)

                        loop = asyncio.get_event_loop()
                        loop.run_until_complete(send_telegram_message(message_text))

                    except Exception as e:
                        # Handle the exception (e.g., log it) and continue with your code
                        print(f"Error sending message to Telegram: {e}")

                return True
            else:
                logging.error("Order placement failed")
        else:
            logging.error("Invalid format for 'index'")
    except Exception as e:
        logging.error(f"{str(e)} while placing order")
    return False
