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
    "^DJI": {"name": "DJ", "weight": 0.35},
    "^IXIC": {"name": "NQ", "weight": 0.30},
    "^GSPC": {"name": "SP", "weight": 0.35},
    "^N225": {"name": "JP", "weight": 0.20},
    "^HSI": {"name": "HK", "weight": 0.20},
    "000001.SS": {"name": "CN", "weight": 0.20},
    "^FTSE": {"name": "UK", "weight": 0.20},
    "^GDAXI": {"name": "DE", "weight": 0.15},
    "^FCHI": {"name": "FR", "weight": 0.15},
    "^NSEI": {"name": "NF", "weight": 0.125},
    "^NSEBANK": {"name": "BK", "weight": 0.125},
    "GIFN50.NS": {"name": "GF", "weight": 0.125}
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

# Print index names with percentage change in one row with sentiment color
index_info = ""
for name, price_today in closing_prices_today.items():
    if name in closing_prices_yesterday:
        price_yesterday = closing_prices_yesterday[name]
        
        # Calculate percentage change
        percentage_change = ((price_today - price_yesterday) / price_yesterday) * 100
        
        # If the index is GIFT, round to 0 decimal places, otherwise to 2 decimals
        if name == "GF":
            percentage_change_str = f"{percentage_change:.0f}"
        else:
            percentage_change_str = f"{percentage_change:.2f}"
        
        # Pad the percentage change string to fit within 5 characters, 
        # adding space before it if necessary.
        padded_change = percentage_change_str.rjust(5)
        
        # Concatenate name and padded percentage change, filling spaces to ensure 7 digits total
        full_string = f"{name}{padded_change}".ljust(7)
        
        # Determine the color based on the sentiment
        sentiment_style = "green" if percentage_change > 0 else "red"
        
        # Add the entire string with the sentiment color
        index_info += f"[{sentiment_style}]{full_string}[/{sentiment_style}]|"

# Print the concatenated string using console.print()
console.print(index_info)

