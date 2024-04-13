import importlib
import subprocess
import time
import warnings
from rich.console import Console
import sys
import os
from cyclepxy import cycle
from clorpxy import RED, GREEN
console = Console()
from sleeppxy import progress_bar
import time
from rich.console import Console
from clorpxy import SILVER, UNDERLINE, RED, GREEN, YELLOW, RESET, BRIGHT_YELLOW, BRIGHT_RED, BRIGHT_GREEN, BOLD, GREY

# Start the script session to capture terminal output
subprocess.run(['script', 'pxy.log'])

# Your main script starts here
from predictpxy import predict_market_sentiment
from mktpxy import get_market_check
from nftpxy import get_nse_action
from utcpxy import peak_time
from macdpxy import calculate_macd_signal
from smapxy import check_index_status

while True:
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')
    
    mktpredict = predict_market_sentiment()
    onemincandlesequance, mktpxy = get_market_check('^NSEI')
    ha_nse_action, nse_power, Day_Change, Open_Change  = get_nse_action()
    peak = peak_time()
    macd = calculate_macd_signal("^NSEI")
    nsma = check_index_status('^NSEI')

    subprocess.run(['python3', 'acvaluepxy.py']) if peak == 'PREPEAK' else None

    print((BRIGHT_GREEN + UNDERLINE + "PXY® PreciseXceleratedYield Pvt Ltd™".center(42) if Open_Change > 0 else (BRIGHT_RED + UNDERLINE + "PXY® PreciseXceleratedYield Pvt Ltd™".center(42) if Open_Change < 0 else BRIGHT_YELLOW + UNDERLINE + "PXY® PreciseXceleratedYield Pvt Ltd™".center(42))) + RESET)

    subprocess.run(['python3', 'daypxy.py']) 
    subprocess.run(['python3', 'buyoptpxy.py']) 
    subprocess.run(['python3', 'buycncpxy.py']) if (not (Open_Change < 0 and Day_Change < 0 and nsma == 'down') and mktpxy == 'Buy') or peak == 'PEAKEND' else None

    subprocess.run(['python3', 'cntrlcncpxy.py']) 
    subprocess.run(['python3', 'cntrloptpxy.py']) 
    subprocess.run(['python3', 'cndlpxy.py'])
    subprocess.run(['python3', 'selfpxy.py'])

    print(f"    PXY® Predicted market sentiment : {mktpredict}")

    cycle
    progress_bar(10, mktpxy)
