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
periods = [1, 2, 3, 4, 5, 6, 7]

# Create a Console instance for rich print formatting
console = Console()

# Function to calculate the Heikin-Ashi candle colors for the last three closed candles
def calculate_last_three_heikin_ashi_colors(symbol, initial_interval='1m', final_interval='15m', settle_periods=3):
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

        # Calculate Heikin-Ashi candles
        ha_close = (data['Open'] + data['High'] + data['Low'] + data['Close']) / 4
        ha_open = (data['Open'].shift(1) + data['Close'].shift(1)) / 2

        # Calculate the colors of the last three closed candles
        current_color = 'Bear' if ha_close.iloc[-1] < ha_open.iloc[-1] else 'Bull'
        last_closed_color = 'Bear' if ha_close.iloc[-2] < ha_open.iloc[-2] else 'Bull'
        second_last_closed_color = 'Bear' if ha_close.iloc[-3] < ha_open.iloc[-3] else 'Bull'

        return current_color, last_closed_color, second_last_closed_color

    except Exception as e:
        console.print(f"[red]Exception occurred: {e}[/red]")
        return 'Error', 'Error', 'Error'

# Function to determine the market check based on candle colors
def get_market_check(symbol):
    # Check the colors of the last two closed candles and the currently running candle
    current_color, last_closed_color, second_last_closed_color = calculate_last_three_heikin_ashi_colors(symbol, intervals[0])

    # Initialize messages
    title = ""

    # Define styles for rich.print
    bear_style = Style(color="red")
    bull_style = Style(color="green")
    buy_style = Style(color="green")
    sell_style = Style(color="red")

    # Determine the market check based on the candle colors and use rich.print to format output
    if current_color == 'Bear' and last_closed_color == 'Bear':
        mktpxy = 'Bear'
        sktpxy = 'Bear'
        console.print("           🐻🔴🔴🔴 [bold]Bearish sentiment![/bold]🍯💰", style=bear_style)
    elif current_color == 'Bull' and last_closed_color == 'Bull':
        mktpxy = 'Bull'
        sktpxy = 'Bull'
        console.print("           🐂🟢🟢🟢 [bold]Bullish sentiment![/bold]💪💰", style=bull_style)
    elif current_color == 'Bear' and last_closed_color == 'Bull':
        mktpxy = 'Sell'
        sktpxy = 'Sell'
        console.print("                🛒🔴🛬⤵️ [bold]Time to sell![/bold]📉💰", style=sell_style) 
    elif current_color == 'Bull' and last_closed_color == 'Bear':
        mktpxy = 'Buy'
        sktpxy = 'Buy'
        console.print("                  🚀🟢🛫⤴️ [bold]Time to buy![/bold]🌠💰", style=buy_style)
    else:
        mktpxy = 'None'
        console.print("            🌟 [bold]Market on standby![/bold]🍿💰📊")
        sktpxy = 'None'

    return mktpxy, sktpxy

# Call the function and store the result in a variable
mktpxy, sktpxy = get_market_check('^NSEI')  # Capture both return values

# Print the result (you can remove this if not needed)
#print(f"mktpxy: {mktpxy}")


