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
    "NIFTY24Q.NS": {"name": "N24", "weight": 0.20},
    "^TNX": {"name": "US10Y", "weight": 0.05},
    "GC=F": {"name": "Gold", "weight": 0.05},
    "HG=F": {"name": "Copper", "weight": 0.05},
    "^NYFANG": {"name": "Tech", "weight": 0.10},
    "BTC-USD": {"name": "BTC", "weight": 0.05}
}

# Create a console object for rich text output
console = Console()

# Fetch historical closing prices for each exchange
closing_prices_today = {}
closing_prices_yesterday = {}

for exchange, name_weight in exchanges.items():
    try:
        ticker = yf.Ticker(exchange)
        period = "5d" if exchange == "NIFTY24Q.NS" else "1mo"
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
            adjusted_price = int(price_today + adjustment)  # No rounding
            return f"{adjusted_price:4d}"  # Ensure 4 character width
        else:
            return f"{int(price_today):4d}"  # Ensure 4 character width
    else:
        if price_yesterday is not None:
            percentage_change = ((price_today - price_yesterday) / price_yesterday) * 100
            percentage_change_str = f"{percentage_change:+.1f}".rjust(4)  # Ensure 4 character width
            return f"{name}{percentage_change_str}"  # Format title + value
        else:
            return f"{name}    "  # Ensure 4 character width

# Prepare index information strings
first_line = ""
second_line = ""

# Determine which indexes go to the first and second lines
first_line_keys = ["DJ", "NQ", "SP", "JP", "HK", "CN"]

# Split the entries across two lines
for name, price_today in closing_prices_today.items():
    entry = create_entry(name, price_today, closing_prices_yesterday.get(name))
    if entry:
        if name in first_line_keys:
            first_line += f"{entry}|"
        else:
            second_line += f"{entry}|"

# Format each line to fit 6 symbols
def format_line(line):
    parts = line.split('|')
    formatted_lines = []
    for i in range(0, len(parts), 6):
        formatted_lines.append('|'.join(parts[i:i+6]))
    return '\n'.join(formatted_lines)

# Print the formatted lines
if first_line:
    console.print(format_line(first_line.rstrip('|')))
if second_line:
    console.print(format_line(second_line.rstrip('|')))

