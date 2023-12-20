while True:
    import time
    import subprocess
    from nftpxy import nse_action, nse_power
    import warnings
    from rich import print
    from rich.console import Console
    from rich.style import Style
    import sys
    import subprocess
    from rich import print
    from looppxy import loop_duration
    from swchpxy import analyze_stock
    import yfinance as yf
    import os
    import sys
    from selfpxy import get_random_spiritual_message
    random_message = get_random_spiritual_message()

    switch = analyze_stock('^NSEI')

    ############################################"PXY® PreciseXceleratedYield Pvt Ltd™############################################

    # Set the python3IOENCODING environment variable to 'utf-8'
    sys.stdout.reconfigure(encoding='utf-8')

    # Suppress yfinance warnings
    warnings.filterwarnings("ignore", category=FutureWarning)
    warnings.filterwarnings("ignore", category=UserWarning)

    # Specify the stock symbol (NIFTY 50)
    symbol = '^NSEI'

    # Intervals
    intervals = [5, 4, 3, 2, 1]
    periods = [1, 2, 3, 4, 5]

    # Create a Console instance for rich print formatting
    console = Console()

    # Function to calculate the Heikin-Ashi candle colors for the last three closed candles
    def calculate_last_three_heikin_ashi_colors(symbol, interval):
        # Check if the current time is within the specified time range (3:45 AM to 4:00 AM UTC)
        current_utc_time = time.gmtime().tm_hour * 60 + time.gmtime().tm_min

        if 222 <= current_utc_time < 233:
            sys.stdout = open(os.devnull, 'w')
    
            # Download data for the specified number of days (fixed to 5 days)
            data = yf.download(symbol, period="5d")
            
            # Extract today's open, yesterday's close, and current price
            today_open = data['Open'].iloc[-1]
            today_high = data['High'].iloc[-1]
            today_low = data['Low'].iloc[-1]
            current_price = data['Close'].iloc[-1]
            
            yesterday_close = data['Close'].iloc[-2]
            yesterday_open = data['Open'].iloc[-2]
            
            sys.stdout.close()
            sys.stdout = sys.__stdout__
    
            day_open = today_open  # Open of the day
            ltp = current_price  # Last traded price
        
            current_color = 'Bear' if day_open > ltp else 'Bull'
            last_closed_color = 'Bear' if day_open > ltp else 'Bull'


        else:
            # Fetch real-time data for the specified interval
            data = yf.Ticker(symbol).history(period=f'{periods[0]}d', interval=f'{interval}m')

            # Calculate Heikin-Ashi candles
            ha_close = (data['Open'] + data['High'] + data['Low'] + data['Close']) / 4
            ha_open = (data['Open'].shift(1) + data['Close'].shift(1)) / 2

            # Calculate the colors of the last three closed candles
            current_color = 'Bear' if ha_close.iloc[-1] < ha_open.iloc[-1] else 'Bull'
            last_closed_color = 'Bear' if ha_close.iloc[-2] < ha_open.iloc[-2] else 'Bull'

        # print(f'Nifty -> : 3rd:{"🔴🔴🔴" if third_last_closed_color == "Bear" else "🟢🟢🟢"}|2nd:{"🔴🔴🔴" if second_last_closed_color == "Bear" else "🟢🟢🟢"}|1st:{"🔴🔴🔴" if last_closed_color == "Bear" else "🟢🟢🟢"}|now:{"🐻🔴🛬⤵️" if current_color == "Bear" else "🐂🟢🛫⤴️"}')
        return current_color, last_closed_color

    # Function to determine the market check based on candle colors
    def get_market_check(symbol):
        # Check the colors of the last two closed candles and the currently running candle
        current_color, last_closed_color = calculate_last_three_heikin_ashi_colors(symbol, intervals[0])

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
            subprocess.run(['python3', 'cntrlpxy.py'])
            console.print("🐻🔴🔴🔴 [bold]Bearish sentiment![/bold] 🍯💰", style=bear_style)
        elif current_color == 'Bull' and last_closed_color == 'Bull':
            mktpxy = 'Bull'
            subprocess.run(['python3', 'cntrlpxy.py'])
            subprocess.run(['python3', 'buypxy.py']) if nse_action in ("Bullish","Bear","Bull") else None
            console.print("🐂🟢🟢🟢 [bold]Bullish sentiment![/bold] 💪💰", style=bull_style)
        elif current_color == 'Bear' and last_closed_color == 'Bull':
            mktpxy = 'Sell'
            subprocess.run(['python3', 'cntrlpxy.py'])
            console.print("🛒🔴🛬⤵️ [bold]Time to sell![/bold] 📉💰", style=sell_style)
        elif current_color == 'Bull' and last_closed_color == 'Bear':
            mktpxy = 'Buy'
            subprocess.run(['python3', 'cntrlpxy.py'])
            subprocess.run(['python3', 'buypxy.py']) if nse_action in ("Bullish","Bear","Bull") else None
            console.print("🚀🟢🛫⤴️ [bold]Time to buy![/bold] 🌠💰", style=buy_style)
        else:
            mktpxy = 'None'
            console.print("🌟 [bold]Market on standby![/bold] 🍿💰📊")

        return mktpxy        
    print("-" * 42)  
    # Call the function and store the result in a variable
    mktpxy = get_market_check('^NSEI')

    # Print the result (you can remove this if not needed)
    # print(f"mktpxy: {mktpxy}")
    print("-" * 42)   
    print(random_message)
    print("-" * 42)   
    def progress_bar(duration):
        for i in range(duration):
            time.sleep(1)
            print("✨.", end='', flush=True)
        print("\nLets see what happens next!")
    # Make sure loop_duration is defined before calling the function
    progress_bar(loop_duration)

