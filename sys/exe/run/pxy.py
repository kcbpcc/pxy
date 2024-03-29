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
console = Console()
bear_style = Style(color="red")
bull_style = Style(color="green")
sell_style = Style(color="red", blink=True)
buy_style = Style(color="green", blink=True)
green_style = Style(color="bright_green")
red_style = Style(color="bright_red")
standby_style = Style(color="yellow", underline=True)
subprocess.run(['python3', 'cpritepxy.py'])
while True:
    from selfpxy import get_random_spiritual_message
    importlib.reload(sys.modules['selfpxy'])  # Correct the usage
    random_message = get_random_spiritual_message()
    from mktpxy import get_market_check
    importlib.reload(sys.modules['mktpxy'])  # Correct the usage
    onemincandlesequance, mktpxy = get_market_check('^NSEI')
    from nftpxy import nse_action, nse_power, Day_Change, Open_Change, OPTIONS
    importlib.reload(sys.modules['nftpxy'])  # Correct the usage
    from cyclepxy import cycle
    importlib.reload(sys.modules['cyclepxy'])  # Correct the usage
    from utcpxy import peak_time
    importlib.reload(sys.modules['utcpxy'])  # Correct the usage
    peak = peak_time()
    from macdpxy import calculate_macd_signal
    importlib.reload(sys.modules['macdpxy'])  # Correct the usage
    macd = calculate_macd_signal("^NSEI")
    from smapxy import check_index_status
    importlib.reload(sys.modules['smapxy'])  # Correct the usage
    nsma = check_index_status('^NSEI')
    from mktrndpxy import get_market_status_for_symbol
    importlib.reload(sys.modules['mktrndpxy'])
    nmktpxy = get_market_status_for_symbol('^NSEI')
    bmktpxy = get_market_status_for_symbol('^NSEBANK')
    fmktpxy = get_market_status_for_symbol('NIFTY_FIN_SERVICE.NS')
    mmktpxy = get_market_status_for_symbol('NIFTY_MID_SELECT.NS')
    subprocess.run(['python3', 'acvaluepxy.py']) if peak == 'PEAKSTART' else None
    subprocess.run(['python3', 'tistpxy.py'])
    ############################################"PXY® PreciseXceleratedYield Pvt Ltd™############################################ 
    #subprocess.run(['python3', 'buynoptpxy.py']) if peak == 'NONPEAK' else None 
    #subprocess.run(['python3', 'buyboptpxy.py']) if peak == 'NONPEAK' else None 
    #subprocess.run(['python3', 'buypxy.py']) if peak != 'PEAKSTART' and mktpxy == 'Buy' and nsma == 'up' else None
    subprocess.run(['python3', 'cntrlpxy.py']) 
    subprocess.run(['python3', 'cndlpxy.py'])
    console.print("[bold]   PXY® PreciseXceleratedYield Pvt Ltd™   [/bold]",
                style=Style(color="bright_green", underline=True) if mktpxy in ["Buy", "Bull"]
                else Style(color="bright_red", underline=True) if mktpxy in ["Sell", "Bear"]
                else None)
    subprocess.run(['python3', 'worldpxy.py'])
    console.print(random_message)
    import time
    def progress_bar(duration, mktpxy):
        console = Console()
        for _ in range(duration):
            time.sleep(1)
            if mktpxy in ['Bull', 'Buy']:
                console.print('[green]🏛 PXY®   [/]', end='')
            else:
                console.print('[red]🏛 PXY®   [/]', end='')
        console.print()  # Move to the next line after the progress bar
    progress_bar(cycle, mktpxy)

