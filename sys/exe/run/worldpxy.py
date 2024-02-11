import yfinance as yf
from rich.console import Console
from rich.text import Text
import warnings

# Suppress warnings
warnings.filterwarnings("ignore")

# Dictionary of major stock exchanges with weights based on their significance and color codes
exchanges = {
    "^DJI": {"name": "D&J", "color": "blue"},
    "^IXIC": {"name": "Nsdq", "color": "cyan"},
    "^GSPC": {"name": "S&P", "color": "magenta"},
    "^FTSE": {"name": "UK", "color": "yellow"},
    "^GDAXI": {"name": "DE", "color": "green"},
    "^FCHI": {"name": "FR", "color": "red"},
    "^N225": {"name": "JP", "color": "blue"},
    "^HSI": {"name": "HK", "color": "cyan"},
    "000001.SS": {"name": "CN", "color": "magenta"},
    "^NSEI": {"name": "NIFTY", "color": "yellow"}  
}

# Create a console object for rich text output
console = Console()

# Print names of other markets with color codes in one line
other_markets = "|".join([f"[{name_weight['color']}]{name_weight['name']}[/]" for exchange, name_weight in exchanges.items() if name_weight['name'] != "NIFTY"])
console.print(other_markets, f"NIFTY: {nifty_close_today}")



