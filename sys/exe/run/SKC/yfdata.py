import yfinance as yf
from rich import print

def fetch_data(symbol):
    """Fetch historical data for the specified ticker symbol."""
    try:
        data = yf.Ticker(symbol).history(period="5d", interval="1m")
        return data
    except Exception as e:
        print(f"[red]Error fetching data for {symbol}: {e}[/red]")
        return None
