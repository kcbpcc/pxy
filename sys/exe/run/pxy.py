import importlib
import subprocess
import time
import warnings
from rich.console import Console
import sys
import os
from cyclepxy import cycle
from clorpxy import RED, GREEN
from sleeppxy import progress_bar  # Assuming progress_bar is defined in sleeppxy

console = Console()

def clear_screen():
    # Clear the screen by printing ANSI escape code for clearing screen
    print("\033c", end="")

subprocess.run(['python3', 'cpritepxy.py'])

while True:
    # Redirect standard output to a file
    with open('output.log', 'a') as f:
        sys.stdout = f
        
        from predictpxy import predict_market_sentiment
        importlib.reload(sys.modules['predictpxy'])  # Correct the usage
        mktpredict = predict_market_sentiment()

        from mktpxy import get_market_check
        importlib.reload(sys.modules['mktpxy'])  # Correct the usage
        onemincandlesequance, mktpxy = get_market_check('^NSEI')

        from nftpxy import get_nse_action
        importlib.reload(sys.modules['nftpxy'])  # Correct the usage
        ha_nse_action, nse_power, Day_Change, Open_Change = get_nse_action()

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
        progress_bar(cycle, mktpxy)
        
        # Restore standard output
        sys.stdout = sys.__stdout__

    # Softly clear the screen
    clear_screen()

    # Wait for a while before the next iteration
    time.sleep(1)  # Adjust the sleep time according to your needs



