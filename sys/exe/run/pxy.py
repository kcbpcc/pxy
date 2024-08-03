def get_user_input(prompt, default='s'):
    user_input = input(prompt).strip()
    if user_input == '':
        return default
    return user_input

run_type = get_user_input("How do you want to run 🗺️⁀જ✈︎ short/long:")

import subprocess
import time
import warnings
from rich.console import Console
import sys
import os
from clorpxy import RED, GREEN, SILVER, UNDERLINE, RESET, BRIGHT_YELLOW, BRIGHT_RED, BRIGHT_GREEN, BOLD, GREY

console = Console()
subprocess.run(['python3', 'cpritepxy.py'])

def handle_exceptions(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ImportError as e:
            print(f"Import error: {e}")
        except Exception as ex:
            print(f"An error occurred: {ex}")
    return wrapper

while True:
    import importlib

    @handle_exceptions
    def reload_sleeppxy():
        importlib.reload(sys.modules['sleeppxy'])
        from sleeppxy import progress_bar  # Re-import the function

    @handle_exceptions
    def reload_cyclepxy():
        importlib.reload(sys.modules['cyclepxy'])
        from cyclepxy import cycle  # Re-import the function

    @handle_exceptions
    def peak_time_handler():
        importlib.reload(sys.modules['utcpxy'])
        from utcpxy import peak_time
        return peak_time()

    @handle_exceptions
    def predict_market_sentiment_handler():
        importlib.reload(sys.modules['predictpxy'])
        from predictpxy import predict_market_sentiment
        return predict_market_sentiment()

    @handle_exceptions
    def get_market_check_handler(symbol):
        importlib.reload(sys.modules['mktpxy'])
        from mktpxy import get_market_check
        return get_market_check(symbol)

    @handle_exceptions
    def get_nse_action_handler():
        importlib.reload(sys.modules['nftpxy'])
        from nftpxy import get_nse_action
        return get_nse_action()

    @handle_exceptions
    def calculate_macd_signal_handler(symbol):
        from macdpxy import calculate_macd_signal
        return calculate_macd_signal(symbol)

    @handle_exceptions
    def check_index_status_handler(symbol):
        from smapxy import check_index_status
        return check_index_status(symbol)

    # Reload and re-import the necessary modules
    reload_sleeppxy()
    reload_cyclepxy()

    try:
        peak = peak_time_handler()
        if os.name == 'nt':
            os.system('cls')
        else:
            if peak == 'NONPEAK':
                os.system('clear -x')
    except Exception as e:
        print(f"Error handling peak time: {e}")

    try:
        mktpredict = predict_market_sentiment_handler()
    except Exception as e:
        print(f"Error handling market sentiment prediction: {e}")
        mktpredict = None

    try:
        onemincandlesequance, mktpxy = get_market_check_handler('^NSEI')
    except Exception as e:
        print(f"Error handling market check for ^NSEI: {e}")
        onemincandlesequance, mktpxy = "none", "none"

    try:
        bnkonemincandlesequance, bmktpxy = get_market_check_handler('^NSEBANK')
    except Exception as e:
        print(f"Error handling market check for ^NSEBANK: {e}")
        bnkonemincandlesequance, bmktpxy = "none", "none"

    try:
        ha_nse_action, nse_power, Day_Change, Open_Change = get_nse_action_handler()
    except Exception as e:
        print(f"Error handling NSE action: {e}")
        ha_nse_action, nse_power, Day_Change, Open_Change = 0.5, 0.5, 0.5, 0.5

    try:
        macd = calculate_macd_signal_handler("^NSEI")
    except Exception as e:
        print(f"Error handling MACD signal calculation: {e}")
        macd = None

    try:
        nsma = check_index_status_handler('^NSEI')
        bsma = check_index_status_handler('^NSEBANK')
    except Exception as e:
        print(f"Error handling index status: {e}")
        nsma, bsma = None, None

    # Example usage of the imported modules/functions
    try:
        progress_bar()
        cycle()
    except Exception as e:
        print(f"Error executing progress_bar or cycle: {e}")
    ############################################"PXY® PreciseXceleratedYield Pvt Ltd™############################################     ############################################"PXY® PreciseXceleratedYield Pvt Ltd™############################################ 
    print((BRIGHT_GREEN + "🏛 PXY® PreciseXceleratedYield Pvt Ltd™ 🏛".center(42) if ha_nse_action == 'Bullish' else BRIGHT_RED + "🏛 PXY® PreciseXceleratedYield Pvt Ltd™ 🏛".center(42) if ha_nse_action == 'Bearish' else "🏛 PXY® PreciseXceleratedYield Pvt Ltd™ 🏛".center(42)) + RESET)    
    print("*" * 42)
    subprocess.run(['python3', 'tistpxy.py']) 
    subprocess.run(['python3', 'cntrloptpxy.py'] if run_type == 'l' else ['python3', 'cntrloptpxy.py', '-short'])
    ############################################"PXY® PreciseXceleratedYield Pvt Ltd™############################################     ############################################"PXY® PreciseXceleratedYield Pvt Ltd™############################################ 
    subprocess.run(['python3', 'telvalpxy.py']) if peak == "PEAKSTART" else None
    if bmktpxy in ['Buy', 'Sell']:
        importlib.reload(sys.modules.get('mktpxy', None))
        print("━" * 42)
        subprocess.run(['python3', 'buyboptpxy.py'])
    else:
        print("━" * 42)
        print(f"{'Not Buying BANK opts ⛔ it is ' + bmktpxy + ' ⚠️':>41}")
    if mktpxy in ['Buy', 'Sell']:
        importlib.reload(sys.modules.get('mktpxy', None))
        print("━" * 42)
        subprocess.run(['python3', 'buynoptpxy.py'])
    else:
        print("━" * 42)
        print(f"{'Not Buying NIFTY opts ⛔ it is ' + mktpxy + ' ⚠️':>41}")
    subprocess.run(['python3', 'worldpxy.py']) if run_type == 'l' else None
    if (peak == 'PEAKEND' or peak == 'PEAKSTART') and ha_nse_action == 'Bullish':
        subprocess.run(['python3', 'buycncpxy.py'])
    ############################################"PXY® PreciseXceleratedYield Pvt Ltd™############################################     ############################################"PXY® PreciseXceleratedYield Pvt Ltd™############################################ 
    if run_type == 'l':
        subprocess.run(['python3', 'niftychartpxy.py'])
        subprocess.run(['python3', 'daypxy.py'])
        subprocess.run(['python3', 'cndlpxy.py'])
        
        if 'nsma' in locals():
            color = BRIGHT_GREEN if nsma == "up" else BRIGHT_RED if nsma == "down" else BRIGHT_YELLOW
            print(color + "ﮩ٨ﮩ٨ـﮩ٨ﮩ٨ـﮩ٨ـﮩﮩ٨ﮩ٨NIFTY٨ﮩ٨ـﮩ٨ـﮩﮩ٨ﮩ٨ـﮩ٨ﮩ٨ـﮩ" + RESET)
        
        subprocess.run(['python3', 'bniftychartpxy.py'])
        subprocess.run(['python3', 'bdaypxy.py'])
        subprocess.run(['python3', 'bcndlpxy.py'])
        
        if 'bsma' in locals():
            color = BRIGHT_GREEN if bsma == "up" else BRIGHT_RED if bsma == "down" else BRIGHT_YELLOW
            print(color + "ﮩ٨ﮩ٨ـﮩ٨ﮩ٨ـﮩ٨ـﮩﮩ٨BANKNIFTY٨ﮩ٨ـﮩ٨ـﮩﮩ٨ﮩ٨ـﮩ٨ﮩ٨" + RESET)
    ############################################"PXY® PreciseXceleratedYield Pvt Ltd™############################################    ############################################"PXY® PreciseXceleratedYield Pvt Ltd™############################################ 
    print("━" * 42)
    if mktpredict in ['FALL', 'SIDE']:
        print(f"{UNDERLINE}{'💥💥  જ⁀➴ CNC Action - NIFTY on FALL  જ⁀➴':>38}{RESET}")
        subprocess.run(['python3', 'cntrlcncpxy.py'])
    else:
        print(f"{'✅ ✅ No Action - NIFTY on RISE  🆙 🆙':>38}")
    ############################################"PXY® PreciseXceleratedYield Pvt Ltd™############################################    ############################################"PXY® PreciseXceleratedYield Pvt Ltd™############################################ 
    subprocess.run(['python3', 'plpxy.py']) if peak == "PEAKEND" else None
    print("━" * 42)
    if run_type == 's':
        #subprocess.run(['python3', 'mngoptpxy.py', 's'])
        subprocess.run(['python3', 'cntrloptprntpxy.py', 's'])
    elif run_type == 'l':
        #subprocess.run(['python3', 'mngoptpxy.py', 'l'])
        subprocess.run(['python3', 'cntrloptprntpxy.py', 'l'])
    print("━" * 42)
    subprocess.run(['python3', 'selfpxy.py'])
    progress_bar(cycle, (mktpxy if peak in ["PEAKSART", "PEAKEND", "NONPEAK"] else None))
    ############################################"PXY® PreciseXceleratedYield Pvt Ltd™############################################    ############################################"PXY® PreciseXceleratedYield Pvt Ltd™############################################ 
