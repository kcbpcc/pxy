import importlib
import subprocess
import time
import warnings
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
    print(f"Cycle 🎡 : {cycle} seconds".rjust(40))
    subprocess.run(['python3', 'tistpxy.py'])
    ############################################"PXY® PreciseXceleratedYield Pvt Ltd™############################################
    # Determine the market check based on the candle colors and use rich.print to format output
    if mktpxy == 'Bear':
        print("It's a 🔴-Bear-🔴 time, selling now.....")
        subprocess.run(['python3', 'cntrlpxy.py'])
        console.print(f"|📅{Day_Change}|⌛️{Open_Change}|⚡{nse_power}|[bold]Bearish sentiment![/bold]", style=bear_style)
    elif mktpxy == 'Bull':
        print("It's a 🟢-Bull-🟢 time, Buying now......")
        subprocess.run(['python3', 'cntrlpxy.py'])
        console.print(f"|📅{Day_Change}|⌛️{Open_Change}|⚡{nse_power}|[bold]Bullish sentiment![/bold]", style=bull_style)
    elif mktpxy == 'Sell':
        print("It's a ⤵️-Sell-⤵️ time, selling now.....")
        subprocess.run(['python3', 'cntrlpxy.py'])
        console.print(f"|📅{Day_Change}|⌛️{Open_Change}|⚡{nse_power}|[bold].....Time to sell![/bold]", style=sell_style)
    elif mktpxy == 'Buy':
        print("It's a ⤴️-Buy-⤴️ time, Buying now.......")
        subprocess.run(['python3', 'buypxy.py'])
        subprocess.run(['python3', 'cntrlpxy.py'])
        console.print(f"|📅{Day_Change}|⌛️{Open_Change}|⚡{nse_power}|[bold]......Time to buy![/bold]", style=buy_style)
    elif mktpxy == 'None':
        subprocess.run(['python3', 'cntrlpxy.py'])
        console.print(f"|📅{Day_Change}|⌛️{Open_Change}|⚡{nse_power}|[bold]..Market on standby![/bold]")
    # Call the function and store the result in a variable
    #subprocess.run(['python3', 'tistpxy.py'])  # Run 'tistpxy.py' using subprocess
    subprocess.run(['python3', 'cndlpxy.py'])  # Run 'cndlpxy.py' using subprocess
    subprocess.run(['python3', 'tistpxy.py'])
    console.print(onemincandlesequance)  # Print the content of 'onemincandlesequance' using the 'console.print' method
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
    def progress_bar(duration, optpxy):
        for i in range(duration):
            time.sleep(1)
            print(optpxy, end='', flush=True)
    # Make sure cycle is defined before calling the function
    progress_bar(cycle, optpxy)
