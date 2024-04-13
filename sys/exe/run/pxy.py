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

subprocess.run(['python3', 'cpritepxy.py'])
def append_terminal_contents_to_log():
    # Get the current directory where the script is located
    current_directory = os.getcwd()
    # Construct the path to the pxy.log file in the current directory
    log_file_path = os.path.join(current_directory, "pxy.log")
    # Use the 'echo' command to append the current tty to pxy.log
    os.system(f'echo "$(tty)" >> {log_file_path}')
while True:
    append_terminal_contents_to_log()
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')
    from predictpxy import predict_market_sentiment
    importlib.reload(sys.modules['predictpxy'])  # Correct the usage
    mktpredict = predict_market_sentiment()
    from mktpxy import get_market_check
    importlib.reload(sys.modules['mktpxy'])  # Correct the usage
    onemincandlesequance, mktpxy = get_market_check('^NSEI')
    from nftpxy import get_nse_action
    importlib.reload(sys.modules['nftpxy'])  # Correct the usage
    ha_nse_action, nse_power, Day_Change, Open_Change  = get_nse_action()
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
    ############################################"PXY® PreciseXceleratedYield Pvt Ltd™############################################
    subprocess.run(['python3', 'acvaluepxy.py']) if peak == 'PREPEAK' else None
    ############################################"PXY® PreciseXceleratedYield Pvt Ltd™############################################ 
    print((BRIGHT_GREEN + UNDERLINE + "PXY® PreciseXceleratedYield Pvt Ltd™".center(42) if Open_Change > 0 else (BRIGHT_RED + UNDERLINE + "PXY® PreciseXceleratedYield Pvt Ltd™".center(42) if Open_Change < 0 else BRIGHT_YELLOW + UNDERLINE + "PXY® PreciseXceleratedYield Pvt Ltd™".center(42))) + RESET)
    subprocess.run(['python3', 'worldpxy.py']) 
    subprocess.run(['python3', 'buyoptpxy.py']) 
    subprocess.run(['python3', 'buycncpxy.py']) if (not (Open_Change < 0 and Day_Change < 0 and nsma == 'down') and mktpxy == 'Buy') or peak == 'PEAKEND' else None
    ############################################"PXY® PreciseXceleratedYield Pvt Ltd™############################################ 
    subprocess.run(['python3', 'cntrlcncpxy.py']) 
    subprocess.run(['python3', 'cntrloptpxy.py']) 
    subprocess.run(['python3', 'cndlpxy.py'])
    subprocess.run(['python3', 'selfpxy.py'])
    subprocess.run(['python3', 'daypxy.py']) 
    print(f"    PXY® Predicted market sentiment : {mktpredict}")
    ############################################"PXY® PreciseXceleratedYield Pvt Ltd™############################################ 
    cycle
    progress_bar(4, mktpxy)


