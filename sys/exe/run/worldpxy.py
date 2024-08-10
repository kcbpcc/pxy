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
    "^DJI": {"name": "DJ", "weight": 0.20},
    "^IXIC": {"name": "NQ", "weight": 0.20},
    "^GSPC": {"name": "SP", "weight": 0.20},
    "^N225": {"name": "JP", "weight": 0.10},
    "^HSI": {"name": "HK", "weight": 0.10},
    "000001.SS": {"name": "CN", "weight": 0.10},
    "^FTSE": {"name": "UK", "weight": 0.05},
    "^GDAXI": {"name": "DE", "weight": 0.05},
    "^FCHI": {"name": "FR", "weight": 0.05},
    "^NSEBANK": {"name": "BK", "weight": 0.05},
    "^NSEI": {"name": "NF", "weight": 0.05},
    "NIFTY24Q.NS": {"name": "N24", "weight": 0.20},  # NIFTY24Q.NS
    "^TNX": {"name": "US10Y", "weight": 0.05},       # U.S. 10-Year Treasury Yield
    "GC=F": {"name": "Gold", "weight": 0.05},         # Gold Prices
    "HG=F": {"name": "Copper", "weight": 0.05},       # Copper Prices
    "^NYFANG": {"name": "Tech", "weight": 0.10},      # Technology Index
    "BTC-USD": {"name": "BTC", "weight": 0.05}        # Bitcoin
}

# Create a console object for rich text output
console = Console()

# Fetch historical closing prices for each exchange
closing_prices_today = {}
closing_prices_yesterday = {}

for exchange, name_weight in exchanges.items():
    try:
        ticker = yf.Ticker(exchange)
        period = "5d" if exchange == "NIFTY24Q.NS" else "1mo"  # Use 5d for NIFTY24Q.NS
        hist_data = ticker.history(period=period)
        
        if len(hist_data) >= 2:
            closing_prices_today[name_weight['name']] = hist_data['Close'][-1]
            closing_prices_yesterday[name_weight['name']] = hist_data['Close'][-2]
        elif exchange == "NIFTY24Q.NS" and len(hist_data) == 1:
            closing_prices_today[name_weight['name']] = hist_data['Close'].iloc[-1]
        else:
            print(f"Warning: Not enough data for {exchange}. Skipping...")
    except Exception as e:
        print(f"Error retrieving data for {exchange}: {e}")
        continue

# Debugging print statements
print("Closing prices today:", closing_prices_today)
print("Closing prices yesterday:", closing_prices_yesterday)

# Function to create formatted entry
def create_entry(name, price_today, price_yesterday=None):
    if name == "N24":  # Special case for NIFTY24Q.NS
        weighted_sum = 0
        total_weight = 0
        for key, value in closing_prices_today.items():
            if key != "N24" and key in exchanges:
                weighted_sum += value * exchanges[key]['weight']
                total_weight += exchanges[key]['weight']
        if total_weight > 0:
            adjustment = (weighted_sum / total_weight) / 100
            adjusted_price = int(price_today + adjustment)
            return f"{adjusted_price}✍️"
        else:
            return f"{price_today}✍️"
    else:
        if price_yesterday is not None:
            percentage_change = ((price_today - price_yesterday) / price_yesterday) * 100
            percentage_change_str = f"+{percentage_change:.1f}" if percentage_change > 0 else f"{percentage_change:.1f}"
            entry = f"{name}{percentage_change_str}".rjust(6)
            sentiment_style = "green" if percentage_change > 0 else "red"
            return f"[{sentiment_style}]{entry}[/{sentiment_style}]"
        else:
            return f"{name} Data Unavailable"

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
    console.print(second_line.rstrip('|'))


