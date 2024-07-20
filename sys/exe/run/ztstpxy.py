import asyncio
from telegram import Bot

# Replace with your actual bot token and chat ID
bot_token = '6867988078:AAGNBJqs4Rf8MR4xPGoL1-PqDOYouPan7b0'
chat_id = '-4136531362'

async def send_test_message():
    bot = Bot(token=bot_token)
    symbol = 'TCS'  # Define the trading symbol or replace with your desired value
    message = (
        f"🔍 Check it out on TradingView: [TradingView](https://www.tradingview.com/chart/?symbol={symbol})\n"
    )
    await bot.send_message(chat_id=chat_id, text=message, parse_mode='Markdown')

if __name__ == "__main__":
    asyncio.run(send_test_message())
