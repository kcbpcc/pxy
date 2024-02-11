import requests
from bs4 import BeautifulSoup
from rich.console import Console
from rich.style import Style

# Function to fetch closing price for a given exchange
def fetch_closing_price(exchange):
    url = f"https://finance.yahoo.com/quote/%5E{exchange}/"
    response = requests.get(url)
    closing_price = None

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        closing_price_element = soup.find("span", {"data-reactid": "50"})
        if closing_price_element:
            closing_price = float(closing_price_element.text.strip().replace(",", ""))
    return closing_price

# Function to determine sentiment based on closing prices
def calculate_sentiment(today_close, yesterday_close):
    if today_close > yesterday_close:
        return "Bullish"
    elif today_close < yesterday_close:
        return "Bearish"
    else:
        return "Neutral"

# Dictionary of major stock exchanges with weights based on their significance
exchanges = {
    "DJI": {"name": "Dow Jones", "weight": 0.35},
    "IXIC": {"name": "Nasdaq", "weight": 0.30},
    "INX": {"name": "S&P 500", "weight": 0.35},
    "FTSE": {"name": "FTSE 100", "weight": 0.20},
    "GDAXI": {"name": "DAX", "weight": 0.15},
    "FCHI": {"name": "CAC 40", "weight": 0.15},
    "N225": {"name": "Nikkei 225", "weight": 0.20},
    "HSI": {"name": "Hang Seng Index", "weight": 0.20},
    "000001.SS": {"name": "Shanghai Composite", "weight": 0.20}
}

# Create a console object for rich text output
console = Console()

# Fetch closing prices for each exchange
closing_prices_today = {}
closing_prices_yesterday = {}

for exchange, name_weight in exchanges.items():
    closing_prices_today[name_weight['name']] = fetch_closing_price(exchange)
    # Assuming yesterday's close is not available, you can manually input the value
    # Or you can fetch it from an external source if available
    closing_prices_yesterday[name_weight['name']] = 0  # Update this with yesterday's closing prices

# Print index names in one row with sentiment color
index_info = ""
for name, price_today in closing_prices_today.items():
    price_yesterday = closing_prices_yesterday[name]
    if price_yesterday != 0:
        sentiment = calculate_sentiment(price_today, price_yesterday)
        sentiment_style = "green" if sentiment == "Bullish" else "red" if sentiment == "Bearish" else "default"
        index_info += f"[color({sentiment_style})]{name}[/{sentiment_style}]  "

# Print all index names in one row with sentiment color
console.print(index_info)


