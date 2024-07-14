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
subprocess.run(['python3', 'cpritepxy.py'])
import os
import importlib
while True:

    try:
        from utcpxy import peak_time
        importlib.reload(sys.modules['utcpxy'])  # Correct the usage
        peak = peak_time()
        if os.name == 'nt':
            os.system('cls')
        else:
            if peak == 'NONPEAK':
                os.system('clear -x')
    except ImportError as e:
        print(f"Import error for utcpxy: {e}")
        # Handle ImportError for utcpxy if needed
    except Exception as ex:
        print(f"An error occurred for utcpxy: {ex}")
        # Handle other exceptions for utcpxy if needed
    
    try:
        from predictpxy import predict_market_sentiment
        importlib.reload(sys.modules['predictpxy'])  # Correct the usage
        mktpredict = predict_market_sentiment()
    except ImportError as e:
        print(f"Import error for predictpxy: {e}")
        # Handle ImportError for predictpxy if needed
    except Exception as ex:
        print(f"An error occurred for predictpxy: {ex}")
        mktpredict = None  # Assign mktpredict to None in case of any exception
    
    try:
        from mktpxy import get_market_check
        importlib.reload(sys.modules['mktpxy'])  # Correct the usage
        onemincandlesequance, mktpxy = get_market_check('^NSEI')
    except Exception as e:
        print("An error occurred for mktpxy:", e)
        onemincandlesequance, mktpxy = "none", "none"
    
    try:
        bnkonemincandlesequance, bmktpxy = get_market_check('^NSEBANK')
    except Exception as e:
        print("An error occurred for mktpxy (NSEBANK):", e)
        bnkonemincandlesequance, bmktpxy = "none", "none"
    
    try:
        from nftpxy import get_nse_action
        importlib.reload(sys.modules['nftpxy'])  # Correct the usage
        ha_nse_action, nse_power, Day_Change, Open_Change = get_nse_action()
    except Exception as e:
        print("An error occurred for nftpxy:", e)
        ha_nse_action, nse_power, Day_Change, Open_Change = 0.5, 0.5, 0.5, 0.5
    
    try:
        from cyclepxy import cycle
    except ImportError as e:
        print(f"Import error for cyclepxy: {e}")
        # Handle ImportError for cyclepxy if needed
    except Exception as ex:
        print(f"An error occurred for cyclepxy: {ex}")
        # Handle other exceptions for cyclepxy if needed
    
    try:
        importlib.reload(sys.modules['cyclepxy'])  # Correct the usage
    except ImportError as e:
        print(f"Import error for cyclepxy reload: {e}")
        # Handle ImportError for cyclepxy reload if needed
    except Exception as ex:
        print(f"An error occurred for cyclepxy reload: {ex}")
        # Handle other exceptions for cyclepxy reload if needed
    
    try:
        from macdpxy import calculate_macd_signal
        macd = calculate_macd_signal("^NSEI")
    except ImportError as e:
        print(f"Import error for macdpxy: {e}")
        # Handle ImportError for macdpxy if needed
    except Exception as ex:
        print(f"An error occurred for macdpxy: {ex}")
        # Handle other exceptions for macdpxy if needed
    
    try:
        importlib.reload(sys.modules['macdpxy'])  # Correct the usage
    except ImportError as e:
        print(f"Import error for macdpxy reload: {e}")
        # Handle ImportError for macdpxy reload if needed
    except Exception as ex:
        print(f"An error occurred for macdpxy reload: {ex}")
        # Handle other exceptions for macdpxy reload if needed
    
    try:
        from smapxy import check_index_status
        nsma = check_index_status('^NSEI')
        bsma = check_index_status('^NSEBANK')
    except ImportError as e:
        print(f"Import error for smapxy: {e}")
        # Handle ImportError for smapxy if needed
    except Exception as ex:
        print(f"An error occurred for smapxy: {ex}")
        # Handle other exceptions for smapxy if needed
    
    try:
        importlib.reload(sys.modules['smapxy'])  # Correct the usage
    except ImportError as e:
        print(f"Import error for smapxy reload: {e}")
        # Handle ImportError for smapxy reload if needed
    except Exception as ex:
        print(f"An error occurred for smapxy reload: {ex}")
        # Handle other exceptions for smapxy reload if needed

    ############################################"PXY® PreciseXceleratedYield Pvt Ltd™############################################ 
    print((BRIGHT_GREEN + UNDERLINE + "🏛 PXY® PreciseXceleratedYield Pvt Ltd™ 🏛".center(42) if mktpredict == 'RISE' else (BRIGHT_RED + UNDERLINE + "🏛 PXY® PreciseXceleratedYield Pvt Ltd™ 🏛".center(42) if mktpredict == 'FALL' else (BRIGHT_YELLOW + UNDERLINE + "🏛 PXY® PreciseXceleratedYield Pvt Ltd™ 🏛".center(42) if mktpredict == 'SIDE' else ""))) + RESET)
    subprocess.run(['python3', 'tistpxy.py'])
    subprocess.run(['python3', 'cntrloptpxy.py']) if 'mktpxy' in ['Buy', 'Sell'] or 'bmktpxy' in ['Buy', 'Sell'] else None
    (lambda: print((GREEN if nsma == "up" else RED if nsma == "down" else YELLOW) + "ﮩ٨ﮩ٨ـﮩ٨ﮩ٨ـﮩ٨ـﮩﮩ٨ﮩ٨NIFTY٨ﮩ٨ـﮩ٨ـﮩﮩ٨ﮩ٨ـﮩ٨ﮩ٨ـﮩ" + RESET))() if 'nsma' in locals() else None
    subprocess.run(['python3', 'buynftbnkpxy.py']) if (peak == 'PEAKEND' and (mktpredict == 'RISE' or mktpredict == 'SIDE')) else None
    subprocess.run(['python3', 'cndlpxy.py'])
    subprocess.run(['python3', 'daypxy.py'])
    subprocess.run(['python3', 'niftychartpxy.py'])
    subprocess.run(['python3', 'worldpxy.py'])
    subprocess.run(['python3', 'bniftychartpxy.py'])
    subprocess.run(['python3', 'bdaypxy.py']) 
    subprocess.run(['python3', 'bcndlpxy.py'])
    (lambda: print((GREEN if bsma == "up" else RED if bsma == "down" else YELLOW) + "ﮩ٨ﮩ٨ـﮩ٨ﮩ٨ـﮩ٨ـﮩﮩ٨BANKNIFTY٨ﮩ٨ـﮩ٨ـﮩﮩ٨ﮩ٨ـﮩ٨ﮩ٨" + RESET))() if 'bsma' in locals() else None    
    subprocess.run(['python3', 'cntrloptpxy.py'])
    subprocess.run(['python3', 'buynoptpxy.py'])
    subprocess.run(['python3', 'buyboptpxy.py'])
    subprocess.run(['python3', 'buyvolcncpxy.py']) if (peak == 'PEAKEND' and (mktpredict == 'RISE' or mktpredict == 'SIDE')) else None
    ############################################"PXY® PreciseXceleratedYield Pvt Ltd™############################################
    subprocess.run(['python3', 'cntrlcncpxy.py'])
    print((BRIGHT_GREEN + UNDERLINE + "🏛 PXY® PreciseXceleratedYield Pvt Ltd™ 🏛".center(42) if mktpredict == 'RISE' else (BRIGHT_RED + UNDERLINE + "🏛 PXY® PreciseXceleratedYield Pvt Ltd™ 🏛".center(42) if mktpredict == 'FALL' else (BRIGHT_YELLOW + UNDERLINE + "🏛 PXY® PreciseXceleratedYield Pvt Ltd™ 🏛".center(42) if mktpredict == 'SIDE' else ""))) + RESET)
    subprocess.run(['python3', 'selfpxy.py'])
    subprocess.run(['python3', 'gooboradpxy.py'])
    ############################################"PXY® PreciseXceleratedYield Pvt Ltd™############################################
    progress_bar(cycle, mktpxy)
