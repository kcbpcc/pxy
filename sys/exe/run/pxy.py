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

# Custom stream class to duplicate output to both terminal and log file
class Tee(object):
    def __init__(self, *files):
        self.files = files

    def write(self, obj):
        for file in self.files:
            file.write(obj)
            file.flush()  # Make sure to flush the buffer to ensure immediate writing

    def flush(self):
        for file in self.files:
            file.flush()

# Open the log file in append mode
with open("pxy.log", "a") as log_file:
    # Redirect standard output to both terminal and log file using Tee
    sys.stdout = Tee(sys.stdout, log_file)

    subprocess.run(['python3', 'cpritepxy.py'])

    while True:
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')

        # Capture terminal output and append it to the log file
        subprocess.run(['script', '-a', 'pxy.log'], stdout=sys.stdout)

        # Import and reload modules
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
        
        subprocess.run(['python3', 'daypxy.py'])
        subprocess.run(['python3', 'buyoptpxy.py'])
        subprocess.run(['python3', 'buycncpxy.py']) if (not (Open_Change < 0 and Day_Change < 0 and nsma == 'down') and mktpxy == 'Buy') or peak == 'PEAKEND' else None
        
        ############################################"PXY® PreciseXceleratedYield Pvt Ltd™############################################
        subprocess.run(['python3', 'cntrlcncpxy.py'])
        subprocess.run(['python3', 'cntrloptpxy.py'])
        subprocess.run(['python3', 'cndlpxy.py'])
        subprocess.run(['python3', 'selfpxy.py'])
        print(f"    PXY® Predicted market sentiment : {mktpredict}")
        ############################################"PXY® PreciseXceleratedYield Pvt Ltd™############################################
        
        cycle
        progress_bar(4, mktpxy)


