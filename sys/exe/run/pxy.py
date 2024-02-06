import importlib
import subprocess
import time
import warnings
from colorama import init, Fore, Style
from rich import print
from rich.console import Console
from rich.style import Style
import sys
import yfinance as yf
import os
from cyclepxy import cycle
from selfpxy import get_random_spiritual_message
random_message = get_random_spiritual_message()
subprocess.run(['python3', 'cpritepxy.py'])
print("━" * 42)
print(random_message)
print("━" * 42)
console = Console()
bear_style = Style(color="red")
bull_style = Style(color="green")
sell_style = Style(color="red", blink=True)
buy_style = Style(color="green", blink=True)
green_style = Style(color="bright_green")
red_style = Style(color="bright_red")
standby_style = Style(color="yellow")  
while True:
    from mktpxy import get_market_check
    importlib.reload(sys.modules['mktpxy'])  # Correct the usage
    onemincandlesequance, mktpxy = get_market_check()
    from nftpxy import nse_action, nse_power, Day_Change, Open_Change, OPTIONS
    importlib.reload(sys.modules['nftpxy'])  # Correct the usage
    from optpxy import get_optpxy
    importlib.reload(sys.modules['optpxy'])  # Correct the usage 
    optpxy = get_optpxy()
    from cyclepxy import cycle
    importlib.reload(sys.modules['cyclepxy'])  # Correct the usage
    from utcpxy import peak_time
    importlib.reload(sys.modules['utcpxy'])  # Correct the usage
    peak = peak_time()
    print(f"Cycle 🎡 : {cycle} seconds".rjust(40))
    subprocess.run(['python3', 'tistpxy.py'])
    from macdpxy import calculate_macd_signal
    importlib.reload(sys.modules['macdpxy'])  # Correct the usage
    macd = calculate_macd_signal("^NSEI")
    ############################################"PXY® PreciseXceleratedYield Pvt Ltd™############################################
    # Determine the market check based on the candle colors and use rich.print to format output
    if mktpxy == 'Bear':
        print("It's a 🔴-Bear-🔴 time, selling now.....")
        subprocess.run(['python3', 'cntrlpxy.py'])
    elif mktpxy == 'Bull':
        print("It's a 🟢-Bull-🟢 time, Buying now......")
        subprocess.run(['python3', 'cntrlpxy.py'])
    elif mktpxy == 'Sell':
        print("It's a ⤵️-Sell-⤵️ time, selling now.....")
        subprocess.run(['python3', 'cntrlpxy.py'])
    elif mktpxy == 'Buy':
        print("It's a ⤴️-Buy-⤴️ time, Buying now.......")
        subprocess.run(['python3', 'buypxy.py']) if nse_power < 0.50 and peak == 'nonpeak' else None
        subprocess.run(['python3', 'cntrlpxy.py'])
    elif mktpxy == 'None':
        subprocess.run(['python3', 'cntrlpxy.py'])
    # Call the function and store the result in a variable
    subprocess.run(['python3', 'optbuypxy.py']) if nse_power < 0.1 or nse_power > 0.9 else None
    subprocess.run(['python3', 'buypxy.py']) if peak == 'peakend' else None
    subprocess.run(['python3', 'cndlpxy.py'])  # Run 'cndlpxy.py' using subprocess 
    try:
        day_change_sign = '+' if Day_Change > 0 else ''
        open_change_sign = '+' if Open_Change > 0 else ''
        # Format the statement with explicit signs and styles
        console.print(f"|🔆{day_change_sign}[{bull_style if Day_Change > 0 else bear_style if Day_Change < 0 else ''}]{Day_Change}[/]|⌛️{open_change_sign}[{bull_style if Open_Change > 0 else bear_style if Open_Change < 0 else ''}]{Open_Change}[/]|⚡{nse_power}|MACD{macd_signal}|{onemincandlesequance}")
    
    except:
        pass  # This will catch any exception and do nothing, continuing with the program
    #subprocess.run(['python3', 'tistpxy.py'])
    print("━" * 42)  # Print another line of 42 dashes
    # console.print("|", style=green_style if mktpxy in ["Buy", "Bull"] else red_style)  # Commented out line
    if optpxy == "Bull":
        console.print("[bold]🏛🏛 PXY® PreciseXceleratedYield Pvt Ltd™ 🏛🏛[/bold]", style=green_style)
    elif optpxy == "Buy":
        console.print("[bold]🏛🏛 PXY® PreciseXceleratedYield Pvt Ltd™ 🏛🏛[/bold]", style=green_style)
    elif optpxy == "Sell":
        console.print("[bold]🏛🏛 PXY® PreciseXceleratedYield Pvt Ltd™ 🏛🏛[/bold]", style=red_style)
    elif optpxy == "Bear":
        console.print("[bold]🏛🏛 PXY® PreciseXceleratedYield Pvt Ltd™ 🏛🏛[/bold]", style=red_style)
    else:
        console.print("🏛🏛 PXY® PreciseXceleratedYield Pvt Ltd™ 🏛🏛", style=standby_style)
    from rich.console import Console
    from rich.style import Style
    import time
    def progress_bar(duration, optpxy):
        console = Console()
        for _ in range(duration):
            time.sleep(1)
            if optpxy in ['Bull', 'Buy']:
                console.print('[green]PXY®[/]', end='')
            else:
                console.print('[red]PXY®[/]', end='')
        console.print()  # Move to the next line after the progress bar
    # Call the function with the desired parameters
    progress_bar(cycle, optpxy)
