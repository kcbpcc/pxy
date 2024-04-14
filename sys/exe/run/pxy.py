import importlib
import subprocess
import time
import warnings
from rich.console import Console
import sys
import os
import logging
from cyclepxy import cycle
from clorpxy import RED, GREEN
console = Console()
from sleeppxy import progress_bar
import time
from rich.console import Console
from clorpxy import SILVER, UNDERLINE, RESET, BRIGHT_YELLOW, BRIGHT_RED, BRIGHT_GREEN, BOLD, GREY
#Configure logging to write all levels of output to both terminal and log file
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),  # Output to terminal
        logging.FileHandler("log.log", mode="a"),  # Output to log file
    ]
)
with open("log.log", "a") as log_file:
    while True:
        from utcpxy import peak_time
        importlib.reload(sys.modules['utcpxy'])  # Correct the usage
        peak = peak_time()
        if os.name == 'nt':
            os.system('cls')
        else:
            if peak == 'NONPEAK':
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
        from macdpxy import calculate_macd_signal
        importlib.reload(sys.modules['macdpxy'])  # Correct the usage
        macd = calculate_macd_signal("^NSEI")
        from smapxy import check_index_status
        importlib.reload(sys.modules['smapxy'])  # Correct the usage
        nsma = check_index_status('^NSEI')
        ############################################"PXY® PreciseXceleratedYield Pvt Ltd™############################################
        subprocess.run(['python3', 'acvaluepxy.py']) if peak == 'PREPEAK' else None
        ############################################"PXY® PreciseXceleratedYield Pvt Ltd™############################################ 
        print((BRIGHT_GREEN + UNDERLINE + "PXY® PreciseXceleratedYield Pvt Ltd™".center(42) if mktpredict == 'RISE' else (BRIGHT_RED + UNDERLINE + "PXY® PreciseXceleratedYield Pvt Ltd™".center(42) if mktpredict == 'FALL' else BRIGHT_YELLOW + UNDERLINE + "PXY® PreciseXceleratedYield Pvt Ltd™".center(42) if mktpredict == 'SIDE' else "")) + RESET)
        subprocess.run(['python3', 'tistpxy.py'])
        subprocess.run(['python3', 'cndlpxy.py'])
        print((GREEN if nsma == "up" else RED if nsma == "down" else YELLOW) + "ﮩ٨ﮩ٨ـﮩ٨ﮩ٨ـﮩ٨ـﮩﮩ٨ﮩ٨ـﮩ٨ﮩ٨ـﮩ٨ـﮩﮩ٨ﮩ٨ـﮩ٨ﮩ٨ـﮩ٨ـﮩ" + RESET)
        subprocess.run(['python3', 'daypxy.py'])
        subprocess.run(['python3', 'buyoptpxy.py'])
        subprocess.run(['python3', 'buycncpxy.py']) if (not (Open_Change < 0 and Day_Change < 0 and nsma == 'down') and mktpxy == 'Buy') or peak == 'PEAKEND' else None
        ############################################"PXY® PreciseXceleratedYield Pvt Ltd™############################################
        subprocess.run(['python3', 'cntrlcncpxy.py'])
        subprocess.run(['python3', 'cntrloptpxy.py'])
        subprocess.run(['python3', 'selfpxy.py'])
        ############################################"PXY® PreciseXceleratedYield Pvt Ltd™############################################
        progress_bar(cycle, mktpxy)

