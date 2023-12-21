
def order_place_avg(index, row):
    try:
       
        exchsym = str(index).split(":")
        
        # Check existing positions
        positions_response = broker.kite.positions()
        open_positions = positions_response.get('net', [])

        existing_position = next((position for position in open_positions if position['tradingsymbol'] == exchsym[1]), None)
        print(f"existing_position: {existing_position}")
        if existing_position:
            logging.info(f"Position already exists for {exchsym[1]}. Skipping order placement.")
            return True

        if len(exchsym) >= 2 :
            logging.info(f"Placing order for {exchsym[1]}, {str(row)}")
            
            # Calculate quantity based on the value of 5000
            qty = 5000 // row['ltp']
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
                
                # No need to calculate remaining available cash in this case

                try:
                    message_text = f"{row['ltp']} \nhttps://www.tradingview.com/chart/?symbol={exchsym[1]}"

                    # Define the bot token and your Telegram username or ID
                    bot_token = '6704281753:AAEed33wBCxEN81n-NUfajo8pm9gcCVxeZg'  # Replace with your actual bot token
                    user_id = '-4093430309'  # Replace with your Telegram user ID

                    # Function to send a message to Telegram
                    async def send_telegram_message(message_text):
                        bot = telegram.Bot(token=bot_token)
                        await bot.send_message(chat_id=user_id, text=message_text)

                    # Send the 'row' content as a message to Telegram immediately after printing the row
                    asyncio.run(send_telegram_message(message_text))

                except Exception as e:
                    # Handle the exception (e.g., log it) and continue with your code
                    print(f"Error sending message to Telegram: {e}")

                return exchsym[1], remaining_cash  # Define remaining_cash appropriately

            return True

        else:
            logging.error("Order placement failed")

    except Exception as e:
        # print(traceback.format_exc())
        logging.error(f"{str(e)} while placing order")

    return False
