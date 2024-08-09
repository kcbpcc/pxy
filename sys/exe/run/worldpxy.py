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
    "^NSEBANK": {"name": "BK", "weight": 0.125},
    "^NSEI": {"name": "NF", "weight": 0.125},
    "NIFTY24Q.NS": {"name": "N24", "weight": 0.10}  # Added NIFTY24Q.NS
}

# Create a console object for rich text output
console = Console()

# Fetch historical closing prices for each exchange
closing_prices_today = {}
closing_prices_yesterday = {}

for exchange, name_weight in exchanges.items():
    ticker = yf.Ticker(exchange)
    hist_data = ticker.history(period="5d")
    
    # Debug: Print fetched data
    print(f"Data for {exchange}:")
    print(hist_data)
    
    if len(hist_data) >= 2:
        closing_prices_today[name_weight['name']] = hist_data['Close'][-1]
        closing_prices_yesterday[name_weight['name']] = hist_data['Close'][-2]
    else:
        print(f"Not enough data for {exchange}")

# Print index names with percentage change in one row with sentiment color
index_info = ""
for name, price_today in closing_prices_today.items():
    if name in closing_prices_yesterday:
        price_yesterday = closing_prices_yesterday[name]
        
        # Calculate percentage change
        percentage_change = ((price_today - price_yesterday) / price_yesterday) * 100
        
        # Format percentage change with 1 decimal place and sign
        if percentage_change > 0:
            percentage_change_str = f"+{percentage_change:.1f}"
        else:
            percentage_change_str = f"{percentage_change:.1f}"
        
        # Construct the entry with exactly 6 characters
        entry = f"{name}{percentage_change_str}".rjust(6)
        
        # Determine the color based on the sentiment
        sentiment_style = "green" if percentage_change > 0 else "red"
        
        # Add the entire string with the sentiment color
        index_info += f"[{sentiment_style}]{entry}[/{sentiment_style}]|"

# Print the concatenated string using console.print() without extra space around |
if index_info:
    console.print(index_info.rstrip('|'))
else:
    print("No index information available.")

