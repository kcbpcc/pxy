import telegram
import asyncio

async def send_telegram_message(message_text):
    try:
        bot_token = '6924826872:AAHTiMaXmjyYbGsCFhdZlRRXkyfZTpsKPug'
        user_usernames = '-4135910842'

        bot = telegram.Bot(token=bot_token)

        await bot.send_message(chat_id=user_usernames, text=message_text)

    except Exception as e:
        print(f"Error sending message to Telegram: {e}")

async def main():
    message_text = "Hello from the main function!"
    
    # Call the send_telegram_message function
    await send_telegram_message(message_text)

# Define async function to run main function
async def run_main():
    await main()

# Run the main asynchronous function
asyncio.run(run_main())
