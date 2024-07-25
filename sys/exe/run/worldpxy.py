#PXY® 
print("━" * 42)
import yfinance as yf
from rich.console import Console
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
    "^IXIC": {"name": "N&Q", "weight": 0.30},
    "^GSPC": {"name": "S&P", "weight": 0.35},
    "^N225": {"name": "JP", "weight": 0.20},
    "^HSI": {"name": "HK", "weight": 0.20},
    "000001.SS": {"name": "CN", "weight": 0.20},
    "^FTSE": {"name": "UK", "weight": 0.20},
    "^GDAXI": {"name": "DE", "weight": 0.15},
    "^FCHI": {"name": "FR", "weight": 0.15},
    "^NSEI": {"name": "NIFTY", "weight": 0.125},
    "^NSEBANK": {"name": "BKFTY", "weight": 0.125}
}

# Create a console object for rich text output
console = Console()

# Fetch historical closing prices for each exchange
closing_prices_today = {}
closing_prices_yesterday = {}

for exchange, name_weight in exchanges.items():
    ticker = yf.Ticker(exchange)
    hist_data = ticker.history(period="5d")
    if len(hist_data) >= 2:
        closing_prices_today[name_weight['name']] = hist_data['Close'][-1]
        closing_prices_yesterday[name_weight['name']] = hist_data['Close'][-2]

# Print index names in one row with sentiment color
index_info = ""
for name, price_today in closing_prices_today.items():
    if name in closing_prices_yesterday:
        price_yesterday = closing_prices_yesterday[name]
        sentiment = calculate_sentiment(price_today, price_yesterday)
        sentiment_style = "green" if sentiment == "Bullish" else "red" if sentiment == "Bearish" else "default"
        index_info += f"[{sentiment_style}]{name}[/{sentiment_style}]|"

price_today = None

for exchange, name_weight in exchanges.items():
    ticker = yf.Ticker(exchange)
    if exchange == "^NSEI":  # Check if the exchange is NIFTY
        price_today_float = ticker.history(period="1d")['Close'].iloc[-1]  # Fetch today's last trade price
        # Extract the last four digits of the integer part
        price_today = int(str(int(price_today_float))[-4:])
        break  # Exit loop once NIFTY price is found

# Concatenate index_info and price_today into a single string
output = index_info
# Print the concatenated string using console.print()
console.print(output)
