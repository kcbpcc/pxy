import asyncio
import aiohttp

# Replace with your actual bot token
BOT_TOKEN = "6409002088:AAH9mu0lfjvHl_IgRAgX7YrjJQa2Ew9qaLo"

# Replace with your Telegram username or ID
USER_USERNAME = "-4022487175"

# Replace with the actual path to your file
FILE_PATH = "/home/userland/pxy/sys/exe/run/bordpxy.txt"

async def send_message(username, message, bot_token):
    api_endpoint = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    params = {
        "chat_id": username,
        "text": message,
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(api_endpoint, params=params) as response:
            return await response.text()

async def main():
    with open(FILE_PATH, "r") as file:
        file_content = file.read()
        response = await send_message(USER_USERNAME, file_content, BOT_TOKEN)
        print(response)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())


