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
    "NIFTY24U.NS": {"name": "N24", "weight": 0.10}  # Added NIFTY24U.NS
}

# Create a console object for rich text output
console = Console()

# Fetch historical closing prices for each exchange
closing_prices_today = {}
closing_prices_yesterday = {}

for exchange, name_weight in exchanges.items():
    ticker = yf.Ticker(exchange)
    hist_data = ticker.history(period="5d")
    
    # Check if enough data is available
    if len(hist_data) >= 2:
        closing_prices_today[name_weight['name']] = hist_data['Close'][-1]
        closing_prices_yesterday[name_weight['name']] = hist_data['Close'][-2]
    elif exchange == "NIFTY24U.NS":
        # Special case for NIFTY24U.NS
        closing_prices_today[name_weight['name']] = hist_data['Close'].iloc[-1]

# Function to create formatted entry
def create_entry(name, price_today, price_yesterday=None):
    if name == "N24":  # Special case for NIFTY24U.NS
        rounded_price = round(price_today / 10) * 10
        return f"{int(rounded_price)}✍️"
    else:
        if price_yesterday is not None:
            percentage_change = ((price_today - price_yesterday) / price_yesterday) * 100
            percentage_change_str = f"+{percentage_change:.1f}" if percentage_change > 0 else f"{percentage_change:.1f}"
            entry = f"{name}{percentage_change_str}".rjust(6)
            sentiment_style = "green" if percentage_change > 0 else "red"
            return f"[{sentiment_style}]{entry}[/{sentiment_style}]"
        else:
            return None

# Prepare index information strings
first_line = ""
second_line = ""

# Determine which indexes go to the first and second lines
first_line_keys = ["DJ", "NQ", "SP", "JP", "HK", "CN"]

for name, price_today in closing_prices_today.items():
    if name in first_line_keys:
        entry = create_entry(name, price_today, closing_prices_yesterday.get(name))
        if entry:
            first_line += f"{entry}|"
    else:
        entry = create_entry(name, price_today, closing_prices_yesterday.get(name))
        if entry:
            second_line += f"{entry}|"

# Print the concatenated strings
if first_line:
    console.print(first_line.rstrip('|') + "|")
if second_line:
    console.print(second_line.rstrip('|') )

