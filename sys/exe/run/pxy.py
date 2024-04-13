import importlib
import subprocess
import time
import warnings
import sys
import os
from rich.console import Console
from cyclepxy import cycle
from sleeppxy import progress_bar
from clorpxy import SILVER, UNDERLINE, RED, GREEN, YELLOW, RESET, BRIGHT_YELLOW, BRIGHT_RED, BRIGHT_GREEN, BOLD, GREY
from predictpxy import predict_market_sentiment
from mktpxy import get_market_check
from nftpxy import get_nse_action
from utcpxy import peak_time
from macdpxy import calculate_macd_signal
from smapxy import check_index_status

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
    while True:
        # Duplicate output to both terminal and log file
        tee = Tee(sys.stdout, log_file)
        sys.stdout = tee

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


