import os
import subprocess
import importlib
import sys
from rich.console import Console
from cyclepxy import cycle
from clorpxy import RED, GREEN, YELLOW, RESET, BRIGHT_YELLOW, BRIGHT_RED, BRIGHT_GREEN, UNDERLINE
from sleeppxy import progress_bar
from utcpxy import peak_time
from predictpxy import predict_market_sentiment
from mktpxy import get_market_check
from nftpxy import get_nse_action
from macdpxy import calculate_macd_signal
from smapxy import check_index_status

console = Console()

def reload_module(module_name):
    try:
        importlib.reload(sys.modules[module_name])
    except Exception as e:
        print(f"Error reloading module {module_name}: {e}")

subprocess.run(['python3', 'cpritepxy.py'])
while True:    
    try:
        reload_module('cyclepxy')
        reload_module('clorpxy')
        reload_module('sleeppxy')
        reload_module('utcpxy')
        reload_module('predictpxy')
        reload_module('mktpxy')
        reload_module('nftpxy')
        reload_module('macdpxy')
        reload_module('smapxy')
        
        peak = peak_time()
        if os.name == 'nt':
            os.system('cls')
        else:
            if peak == 'NONPEAK':
                os.system('clear -x')
    except Exception as e:
        print(f"Error in peak time or system clear: {e}")
        peak = None
    
    try:
        mktpredict = predict_market_sentiment()
    except Exception as e:
        print(f"Error predicting market sentiment: {e}")
        mktpredict = None
    
    try:
        onemincandlesequance, mktpxy = get_market_check('^NSEI')
    except Exception as e:
        print(f"Error getting market check: {e}")
        onemincandlesequance, mktpxy = None, None
    
    try:
        ha_nse_action, nse_power, Day_Change, Open_Change = get_nse_action()
    except Exception as e:
        print(f"Error getting NSE action: {e}")
        ha_nse_action, nse_power, Day_Change, Open_Change = None, None, None, None
    
    try:
        cycle_result = cycle()
    except Exception as e:
        print(f"Error in cycle function: {e}")
        cycle_result = None
    
    try:
        macd = calculate_macd_signal("^NSEI")
    except Exception as e:
        print(f"Error calculating MACD signal: {e}")
        macd = None
    
    try:
        nsma = check_index_status('^NSEI')
    except Exception as e:
        print(f"Error checking index status: {e}")
        nsma = None
    
    print((BRIGHT_GREEN + UNDERLINE + "🏛 PXY® PreciseXceleratedYield Pvt Ltd™ 🏛".center(42) if mktpredict == 'RISE' else (BRIGHT_RED + UNDERLINE + "🏛 PXY® PreciseXceleratedYield Pvt Ltd™ 🏛".center(42) if mktpredict == 'FALL' else (BRIGHT_YELLOW + UNDERLINE + "🏛 PXY® PreciseXceleratedYield Pvt Ltd™ 🏛".center(42) if mktpredict == 'SIDE' else ""))) + RESET)
    
    subprocess.run(['python3', 'tistpxy.py'])
    subprocess.run(['python3', 'cndlpxy.py'])
    subprocess.run(['python3', 'worldpxy.py']) 
    subprocess.run(['python3', 'cntrloptpxy.py'])
    subprocess.run(['python3', 'buyboptpxy.py'])
    subprocess.run(['python3', 'buynoptpxy.py'])
    subprocess.run(['python3', 'niftychartpxy.py'])
    
    print((GREEN if nsma == "up" else RED if nsma == "down" else YELLOW) + "ﮩ٨ﮩ٨ـﮩ٨ﮩ٨ـﮩ٨ـﮩﮩ٨ﮩ٨ـﮩ٨ﮩ٨ـﮩ٨ـﮩﮩ٨ﮩ٨ـﮩ٨ﮩ٨ـﮩ٨ـﮩ" + RESET)
    
    subprocess.run(['python3', 'daypxy.py'])
    
    print("━" * 42)
    
    if (mktpxy == "Buy" and peak == 'NONPEAK' and nse_power < 0.35) or peak == 'PEAKEND':
        subprocess.run(['python3', 'buycncpxy.py'])
    
    subprocess.run(['python3', 'cntrlcncpxy.py'])
    
    print("━" * 42)
    
    subprocess.run(['python3', 'selfpxy.py'])
    
    print("━" * 42)
    
    subprocess.run(['python3', 'cntrloptpxy.py'], stdout=open('output.txt', 'w'), stderr=subprocess.PIPE)
    subprocess.run(['python3', 'gooboradpxy.py'])
    
    progress_bar(cycle, mktpxy)

