import importlib
import subprocess
import time
import warnings
from colorama import init, Fore, Style
from rich.console import Console
from rich.style import Style
import sys
import yfinance as yf
import os
from cyclepxy import cycle
subprocess.run(['python3', 'cpritepxy.py'])
console = Console()
bear_style = Style(color="red")
bull_style = Style(color="green")
sell_style = Style(color="red", blink=True)
buy_style = Style(color="green", blink=True)
green_style = Style(color="bright_green")
red_style = Style(color="bright_red")
standby_style = Style(color="yellow")  
while True:
    from selfpxy import get_random_spiritual_message
    importlib.reload(sys.modules['selfpxy'])  # Correct the usage
    random_message = get_random_spiritual_message()
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
    from smaftypxy import check_nifty_status
    importlib.reload(sys.modules['smaftypxy'])  # Correct the usage
    SMAfty = check_nifty_status()
    subprocess.run(['python3', 'cntrlpxy.py'])
    from mktrndpxy import get_market_status_for_symbol
    importlib.reload(sys.modules['mktrndpxy'])
    nmktpxy = get_market_status_for_symbol('^NSEI')
    bmktpxy = get_market_status_for_symbol('^NSEBANK')
    fmktpxy = get_market_status_for_symbol('NIFTY_FIN_SERVICE.NS')
    mmktpxy = get_market_status_for_symbol('NIFTY_MID_SELECT.NS')
    subprocess.run(['python3', 'acvaluepxy.py']) if peak == 'PEAKSTART' else None
    ############################################"PXY® PreciseXceleratedYield Pvt Ltd™############################################    
    subprocess.run(['python3', 'buynoptpxy.py']) if nmktpxy == "Buy" or nmktpxy == "Sell" else None
    subprocess.run(['python3', 'buyboptpxy.py']) if bmktpxy == "Buy" or bmktpxy == "Sell" else None
    subprocess.run(['python3', 'buyfoptpxy.py']) if fmktpxy == "Buy" or fmktpxy == "Sell" else None
    #subprocess.run(['python3', 'buymoptpxy.py']) if mmktpxy == "Buy" or mmktpxy == "Sell" else None
    # Call the function and store the result in a variable
    subprocess.run(['python3', 'buypxy.py']) if peak == 'PEAKEND' else None
    print("━" * 42)  # Print another line of 42 dashes 
    subprocess.run(['python3', 'cntrlpxy.py'])
    subprocess.run(['python3', 'cndlpxy.py']) 
    subprocess.run(['python3', 'worldpxy.py'])
    # Print values with color using rich styles
    console.print(f"█NIFTY:", end="", style=green_style if nmktpxy == 'Buy' else red_style if nmktpxy == 'Sell' else None)
    console.print(f"{nmktpxy}", style=green_style if nmktpxy == 'Buy' else red_style if nmktpxy == 'Sell' else None, highlight=False, end="")
    console.print(f" █BANK:", end="", style=green_style if bmktpxy == 'Buy' else red_style if bmktpxy == 'Sell' else None)
    console.print(f"{bmktpxy}", style=green_style if bmktpxy == 'Buy' else red_style if bmktpxy == 'Sell' else None, highlight=False, end="")
    console.print(f" █FIN:", end="", style=green_style if fmktpxy == 'Buy' else red_style if fmktpxy == 'Sell' else None)
    console.print(f"{fmktpxy}", style=green_style if fmktpxy == 'Buy' else red_style if fmktpxy == 'Sell' else None, highlight=False, end="")
    console.print(f" █MCP:", end="", style=green_style if mmktpxy == 'Buy' else red_style if mmktpxy == 'Sell' else None)
    console.print(f"{mmktpxy}", style=green_style if mmktpxy == 'Buy' else red_style if mmktpxy == 'Sell' else None, highlight=False)
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
    print("━" * 42)
    console.print("[bold]" + random_message + "[/bold]", style=standby_style)
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
    progress_bar(cycle, optpxy)

