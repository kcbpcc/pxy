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
from clorpxy import SILVER, UNDERLINE, RESET, BRIGHT_YELLOW, BRIGHT_RED, BRIGHT_GREEN, BOLD, GREY
subprocess.run(['python3', 'rmtknpxy.py'])
subprocess.run(['python3', 'loginpxy.py'])
subprocess.run(['python3', 'cpritepxy.py'])
while True:
    from utcpxy import peak_time
    importlib.reload(sys.modules['utcpxy'])  # Correct the usage
    peak = peak_time()
    if os.name == 'nt':
        os.system('cls')
    else:
        if peak == 'NONPEAK':
            os.system('clear -x')
    from predictpxy import predict_market_sentiment
    importlib.reload(sys.modules['predictpxy'])  # Correct the usage
    mktpredict = predict_market_sentiment()
    from mktpxy import get_market_check
    try:
        importlib.reload(sys.modules['mktpxy'])  # Correct the usage
        onemincandlesequance, mktpxy = get_market_check('^NSEI')
    except Exception as e:
        print("An error occurred:", e)
        onemincandlesequance = mktpxy = "Buy"
    from nftpxy import get_nse_action
    try:
        importlib.reload(sys.modules['nftpxy'])  # Correct the usage
        ha_nse_action, nse_power, Day_Change, Open_Change = get_nse_action()
    except Exception as e:
        print("An error occurred:", e)
        ha_nse_action = nse_power = Day_Change = Open_Change = 0.5
    from cyclepxy import cycle
    importlib.reload(sys.modules['cyclepxy'])  # Correct the usage
    from macdpxy import calculate_macd_signal
    importlib.reload(sys.modules['macdpxy'])  # Correct the usage
    macd = calculate_macd_signal("^NSEI")
    from smapxy import check_index_status
    importlib.reload(sys.modules['smapxy'])  # Correct the usage
    nsma = check_index_status('^NSEI')
    bsma = check_index_status('^NSEI')
    ############################################"PXY® PreciseXceleratedYield Pvt Ltd™############################################ 
    print((BRIGHT_GREEN + UNDERLINE + "🏛 PXY® PreciseXceleratedYield Pvt Ltd™ 🏛".center(42) if mktpredict == 'RISE' else (BRIGHT_RED + UNDERLINE + "🏛 PXY® PreciseXceleratedYield Pvt Ltd™ 🏛".center(42) if mktpredict == 'FALL' else (BRIGHT_YELLOW + UNDERLINE + "🏛 PXY® PreciseXceleratedYield Pvt Ltd™ 🏛".center(42) if mktpredict == 'SIDE' else ""))) + RESET)
    subprocess.run(['python3', 'tistpxy.py'])
    subprocess.run(['python3', 'worldpxy.py'])
    print((GREEN if nsma == "up" else RED if nsma == "down" else YELLOW) + "ﮩ٨ﮩ٨ـﮩ٨ﮩ٨ـﮩ٨ـﮩﮩ٨ﮩ٨NIFTY٨ﮩ٨ـﮩ٨ـﮩﮩ٨ﮩ٨ـﮩ٨ﮩ٨ـﮩ" + RESET)
    #subprocess.run(['python3', 'niftychartpxy.py'])
    subprocess.run(['python3', 'cndlpxy.py'])
    subprocess.run(['python3', 'daypxy.py'])
    subprocess.run(['python3', 'bdaypxy.py']) 
    subprocess.run(['python3', 'bcndlpxy.py'])
    #subprocess.run(['python3', 'bniftychartpxy.py'])
    print((GREEN if bsma == "up" else RED if bsma == "down" else YELLOW) + "ﮩ٨ﮩ٨ـﮩ٨ﮩ٨ـﮩ٨ـﮩﮩ٨BANKNIFTY٨ﮩ٨ـﮩ٨ـﮩﮩ٨ﮩ٨ـﮩ٨ﮩ٨" + RESET)
    subprocess.run(['python3', 'buyboptpxy.py'])
    subprocess.run(['python3', 'cntrloptpxy.py'])
    #subprocess.run(['python3', 'buycncpxy.py']) if (mktpxy == "Buy" and peak == 'NONPEAK' and nse_power < 0.35) or peak == 'PEAKEND' else None
    
    ############################################"PXY® PreciseXceleratedYield Pvt Ltd™############################################
    subprocess.run(['python3', 'cntrlcncpxy.py'])
    print("━" * 42)
    subprocess.run(['python3', 'selfpxy.py'])
    print("━" * 42)
    subprocess.run(['python3', 'cntrloptpxy.py'], stdout=open('output.txt', 'w'), stderr=subprocess.PIPE)
    subprocess.run(['python3', 'gooboradpxy.py'])
    ############################################"PXY® PreciseXceleratedYield Pvt Ltd™############################################
    progress_bar(cycle, mktpxy)
