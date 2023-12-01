import yfinance as yf
import warnings
from rich import print
from rich.console import Console
import sys
interval_to_check = 5  # Replace with the desired interval in minutes
# Set the PYTHONIOENCODING environment variable to 'utf-8'
sys.stdout.reconfigure(encoding='utf-8')

# Suppress yfinance warnings
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)

# Create a Console instance for rich print formatting
console = Console()

# Function to calculate the Heikin-Ashi candle colors for the last three closed candles
def calculate_last_three_heikin_ashi_colors(symbol, interval):
    # Fetch real-time data for the specified interval
    data = yf.Ticker(symbol).history(period='5d', interval=f'{interval}m')

    # Calculate Heikin-Ashi candles
    ha_close = (data['Open'] + data['High'] + data['Low'] + data['Close']) / 4
    ha_open = (data['Open'].shift(1) + data['Close'].shift(1)) / 2

    # Calculate the colors of the last three closed candles
    current_color = 'Bear' if ha_close.iloc[-1] < ha_open.iloc[-1] else 'Bull'
    last_closed_color = 'Bear' if ha_close.iloc[-2] < ha_open.iloc[-2] else 'Bull'
    second_last_closed_color = 'Bear' if ha_close.iloc[-3] < ha_open.iloc[-3] else 'Bull'

    return current_color, last_closed_color, second_last_closed_color

# Function to determine the market check based on candle colors
def get_market_check(symbol, interval):
    # Check the colors of the last two closed candles and the currently running candle
    current_color, last_closed_color, second_last_closed_color = calculate_last_three_heikin_ashi_colors(symbol, interval)

    # Determine the market check based on the candle colors
    if current_color == 'Bear' and last_closed_color == 'Bear':
        smbpxy = 'Bear'
    elif current_color == 'Bull' and last_closed_color == 'Bull':
        smbpxy = 'Bull'
    elif current_color == 'Bear' and last_closed_color == 'Bull':
        smbpxy = 'Sell'
    elif current_color == 'Bull' and last_closed_color == 'Bear':
        smbpxy = 'Buy'
    else:
        smbpxy = 'None'

    return smbpxy

# Example usage:

result = get_market_check(symbol_to_check, interval_to_check)

