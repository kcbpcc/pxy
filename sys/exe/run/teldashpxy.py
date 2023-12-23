import asyncio
from aiohttp import FormData
import aiohttp

# Replace 'YOUR_BOT_TOKEN' with your actual Telegram bot token
BOT_TOKEN = "6396096532:AAG5adz_SeUwV8WLn7miteljk_pRrpt8mO0"

# Replace 'YOUR_CHAT_ID' with your chat ID
CHAT_ID = -4067167377

# Replace '/home/userland/pxy/sys/exe/run/bordpxy.txt' with the actual path to your file
FILE_PATH = "/home/userland/pxy/sys/exe/run/bordpxy.txt"

async def send_file(chat_id, file_path, bot_token):
    api_endpoint = f"https://api.telegram.org/bot{bot_token}/sendDocument"

    async with aiohttp.ClientSession() as session:
        form_data = FormData()
        form_data.add_field("document", open(file_path, "rb"))
        params = {"chat_id": str(chat_id)}  # Ensure chat_id is a string
        async with session.post(api_endpoint, params=params, data=form_data) as response:
            return await response.text()

async def main():
    response = await send_file(CHAT_ID, FILE_PATH, BOT_TOKEN)
    print(response)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
