def get_user_input(prompt, default='s'):
    user_input = input(prompt).strip()
    if user_input == '':
        return default
    return user_input

def save_output_to_rtf(content, filename='output.rtf'):
    with open(filename, 'w') as file:
        file.write("{\\rtf1\\ansi\n")
        file.write(content.replace('\n', '\\par\n'))
        file.write("\n}")
        
run_type = get_user_input("How do you want to run 🗺️⁀જ✈︎ short/long:")
import importlib
import subprocess
import time
import warnings
from rich.console import Console
import sys
import os
from clorpxy import RED, GREEN
console = Console()
import time
from rich.console import Console
from clorpxy import SILVER, UNDERLINE, RESET, BRIGHT_YELLOW, BRIGHT_RED, BRIGHT_GREEN, BOLD, GREY
subprocess.run(['python3', 'cpritepxy.py'])
import os
import importlib
while True:
    import os
    import sys
    import importlib
    save_output_to_rtf(output_content, 'output.rtf')
    def handle_exceptions(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except ImportError as e:
                print(f"Import error: {e}")
            except Exception as ex:
                print(f"An error occurred: {ex}")
        return wrapper
    @handle_exceptions
    def peak_time_handler():
        from utcpxy import peak_time
        importlib.reload(sys.modules['utcpxy'])  # Reload module after import
        return peak_time()
    @handle_exceptions
    def predict_market_sentiment_handler():
        from predictpxy import predict_market_sentiment
        importlib.reload(sys.modules['predictpxy'])  # Reload module after import
        return predict_market_sentiment()
    @handle_exceptions
    def get_market_check_handler(symbol):
        from mktpxy import get_market_check
        importlib.reload(sys.modules['mktpxy'])  # Reload module after import
        return get_market_check(symbol)
    @handle_exceptions
    def get_nse_action_handler():
        from nftpxy import get_nse_action
        importlib.reload(sys.modules['nftpxy'])  # Reload module after import
        return get_nse_action()
    @handle_exceptions
    def calculate_macd_signal_handler(symbol):
        from macdpxy import calculate_macd_signal
        return calculate_macd_signal(symbol)
    @handle_exceptions
    def check_index_status_handler(symbol):
        from smapxy import check_index_status
        return check_index_status(symbol)
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
    ############################################"PXY® PreciseXceleratedYield Pvt Ltd™############################################     ############################################"PXY® PreciseXceleratedYield Pvt Ltd™############################################ 
    print((BRIGHT_GREEN + UNDERLINE + "🏛 PXY® PreciseXceleratedYield Pvt Ltd™ 🏛".center(42) if mktpredict == 'RISE' else (BRIGHT_RED + UNDERLINE + "🏛 PXY® PreciseXceleratedYield Pvt Ltd™ 🏛".center(42) if mktpredict == 'FALL' else (BRIGHT_YELLOW + UNDERLINE + "🏛 PXY® PreciseXceleratedYield Pvt Ltd™ 🏛".center(42) if mktpredict == 'SIDE' else ""))) + RESET)
    subprocess.run(['python3', 'tistpxy.py']) 
    subprocess.run(['python3', 'cntrloptpxy.py'])
    subprocess.run(['python3', 'buyboptpxy.py'])
    subprocess.run(['python3', 'buynoptpxy.py'])
    if run_type == 's':
        subprocess.run(['python3', 'cntrloptprntpxy.py', 's'])
    elif run_type == 'l':
        subprocess.run(['python3', 'cntrloptprntpxy.py', 'l'])
    subprocess.run(['python3', 'worldpxy.py']) if run_type == 'l' else None
    subprocess.run(['python3', 'buycncpxy.py']) if peak == 'PEAKEND' and (mktpredict in ['RISE'] or Day_Change > 0 or Open_Change > 0) else None
    ############################################"PXY® PreciseXceleratedYield Pvt Ltd™############################################     ############################################"PXY® PreciseXceleratedYield Pvt Ltd™############################################ 
    subprocess.run(['python3', 'niftychartpxy.py']) if run_type == 'l' else None    
    subprocess.run(['python3', 'daypxy.py']) if run_type == 'l' else None  
    subprocess.run(['python3', 'cndlpxy.py']) if run_type == 'l' else None  
    (lambda: print((BRIGHT_GREEN if nsma == "up" else BRIGHT_RED if nsma == "down" else BRIGHT_YELLOW) + "ﮩ٨ﮩ٨ـﮩ٨ﮩ٨ـﮩ٨ـﮩﮩ٨ﮩ٨NIFTY٨ﮩ٨ـﮩ٨ـﮩﮩ٨ﮩ٨ـﮩ٨ﮩ٨ـﮩ" + RESET))() if run_type == 'l' and 'nsma' in locals() else None
    subprocess.run(['python3', 'bniftychartpxy.py']) if run_type == 'l' else None  
    subprocess.run(['python3', 'bdaypxy.py'])  if run_type == 'l' else None  
    subprocess.run(['python3', 'bcndlpxy.py']) if run_type == 'l' else None  
    (lambda: print((BRIGHT_GREEN if bsma == "up" else BRIGHT_RED if bsma == "down" else BRIGHT_YELLOW) + "ﮩ٨ﮩ٨ـﮩ٨ﮩ٨ـﮩ٨ـﮩﮩ٨BANKNIFTY٨ﮩ٨ـﮩ٨ـﮩﮩ٨ﮩ٨ـﮩ٨ﮩ٨" + RESET))() if run_type == 'l' and 'bsma' in locals() else None
    subprocess.run(['python3', 'cntrlcncpxy.py'])
    ############################################"PXY® PreciseXceleratedYield Pvt Ltd™############################################     ############################################"PXY® PreciseXceleratedYield Pvt Ltd™############################################ 
    print((BRIGHT_GREEN + UNDERLINE + "🏛 PXY® PreciseXceleratedYield Pvt Ltd™ 🏛".center(42) if mktpredict == 'RISE' else (BRIGHT_RED + UNDERLINE + "🏛 PXY® PreciseXceleratedYield Pvt Ltd™ 🏛".center(42) if mktpredict == 'FALL' else (BRIGHT_YELLOW + UNDERLINE + "🏛 PXY® PreciseXceleratedYield Pvt Ltd™ 🏛".center(42) if mktpredict == 'SIDE' else ""))) + RESET)
    subprocess.run(['python3', 'selfpxy.py'])
    ############################################"PXY® PreciseXceleratedYield Pvt Ltd™############################################    ############################################"PXY® PreciseXceleratedYield Pvt Ltd™############################################ 
    from sleeppxy import progress_bar
    from cyclepxy import cycle
    subprocess.run(['python3', 'plpxy.py'])
    progress_bar(cycle, (mktpxy if peak in ["PEAKSART", "PEAKEND", "NONPEAK"] else None))
    ############################################"PXY® PreciseXceleratedYield Pvt Ltd™############################################    ############################################"PXY® PreciseXceleratedYield Pvt Ltd™############################################ 





