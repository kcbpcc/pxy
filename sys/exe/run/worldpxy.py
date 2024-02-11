import yfinance as yf
from rich.console import Console
from rich.text import Text
import warnings

# Suppress warnings
warnings.filterwarnings("ignore")

# Function to determine sentiment based on closing prices
def calculate_sentiment(today_close, yesterday_close):
    if today_close is not None and yesterday_close is not None:
        if today_close > yesterday_close:
            return "Bullish"
        elif today_close < yesterday_close:
            return "Bearish"
        else:
            return "Neutral"
    else:
        return "Data Unavailable"

# Dictionary of major stock exchanges with weights based on their significance
exchanges = {
    "^DJI": {"name": "D&J", "weight": 0.35},
    "^IXIC": {"name": "Nsdq", "weight": 0.30},
    "^GSPC": {"name": "S&P", "weight": 0.35},
    "^FTSE": {"name": "UK", "weight": 0.20},
    "^GDAXI": {"name": "DE", "weight": 0.15},
    "^FCHI": {"name": "FR", "weight": 0.15},
    "^N225": {"name": "JP", "weight": 0.20},
    "^HSI": {"name": "HK", "weight": 0.20},
    "000001.SS": {"name": "CN", "weight": 0.20}
}

# Create a console object for rich text output
console = Console()

# Fetch historical closing prices for each exchange
closing_prices_today = {}
closing_prices_yesterday = {}

for exchange, name_weight in exchanges.items():
    ticker = yf.Ticker(exchange)
    hist_data = ticker.history(period="2d")
    if len(hist_data) >= 2:
        closing_prices_today[name_weight['name']] = hist_data['Close'][-1]
        closing_prices_yesterday[name_weight['name']] = hist_data['Close'][-2]

# Generate the formatted string with color formatting based on sentiment
formatted_string = Text()
for name, price_today in closing_prices_today.items():
    if name != "NIFTY":
        sentiment = calculate_sentiment(price_today, closing_prices_yesterday[name])
        if sentiment == "Bullish":
            color = "bold green"
        elif sentiment == "Bearish":
            color = "bold red"
        else:
            color = "bold"
        
        formatted_string.append(f"{name}: ", style=color)
        formatted_string.append(f"{price_today} | ", style=color)
    else:
        sentiment = calculate_sentiment(price_today, closing_prices_yesterday[name])
        if sentiment == "Bullish":
            color = "bold green"
        elif sentiment == "Bearish":
            color = "bold red"
        else:
            color = "bold"
        
        formatted_string.append(f"NIFTY: ", style=color)
        formatted_string.append(f"{price_today}", style=color)

# Print the formatted string
console.print(formatted_string)



