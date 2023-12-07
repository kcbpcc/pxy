import yfinance as yf
import warnings
from rich.console import Console
from rich.style import Style

# Set the PYTHONIOENCODING environment variable to 'utf-8'
import sys
sys.stdout.reconfigure(encoding='utf-8')

# Suppress yfinance warnings
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)

# Specify the stock symbol (NIFTY 50)
symbol = '^NSEI'

# Intervals in minutes
intervals = [15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]

# Create a Console instance for rich print formatting
console = Console()

# Function to calculate the Heikin-Ashi candle colors for the last two closed candles
def calculate_last_two_heikin_ashi_colors(symbol, initial_interval='1m', final_interval='15m'):
    try:
        # Using the initial interval for past and current candle
        initial_data = yf.Ticker(symbol).history(period='1d', interval=initial_interval)

        # Resample to the final interval
        data = initial_data.resample(final_interval).agg({
            'Open': 'first',
            'High': 'max',
            'Low': 'min',
            'Close': 'last',
            'Volume': 'sum'
        })

        ha_close = (data['Open'] + data['High'] + data['Low'] + data['Close']) / 4
        ha_open = (data['Open'].shift(1) + data['Close'].shift(1)) / 2

        current_color = 'Bear' if ha_close.iloc[-1] < ha_open.iloc[-1] else 'Bull'
        last_closed_color = 'Bear' if ha_close.iloc[-2] < ha_open.iloc[-2] else 'Bull'

        return current_color, last_closed_color

# Function to determine the market check based on candle colors
def get_market_check(symbol):
    # Check the colors of the last two closed candles
    current_color, last_closed_color = calculate_last_two_heikin_ashi_colors(symbol, intervals[0])

    # Initialize messages
    title = ""

    # Define styles for rich.print
    bear_style = Style(color="red")
    bull_style = Style(color="green")

    # Determine the market check based on the candle colors and use rich.print to format output
    if current_color == 'Bear' and last_closed_color == 'Bear':
        console.print("           🐻🔴🔴🔴 [bold]Bearish sentiment![/bold]🍯💰", style=bear_style)
    elif current_color == 'Bull' and last_closed_color == 'Bull':
        console.print("           🐂🟢🟢🟢 [bold]Bullish sentiment![/bold]💪💰", style=bull_style)
    elif current_color == 'Bear' and last_closed_color == 'Bull':
        console.print("                🛒🔴🛬⤵️ [bold]Time to sell![/bold]📉💰", style=bear_style)
    elif current_color == 'Bull' and last_closed_color == 'Bear':
        console.print("                  🚀🟢🛫⤴️ [bold]Time to buy![/bold]🌠💰", style=bull_style)
    else:
        console.print("            🌟 [bold]Market on standby![/bold]🍿💰📊")

    return current_color, last_closed_color

# Call the function and store the result in a variable
mktpxy, sktpxy = get_market_check('^NSEI')  # Capture both return values

# Print the result (you can remove this if not needed)
# print(f"mktpxy: {mktpxy}")


