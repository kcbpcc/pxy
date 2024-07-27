import os
import sys
import subprocess
import time
import importlib
from rich.console import Console
from clorpxy import RED, GREEN, SILVER, UNDERLINE, RESET, BRIGHT_YELLOW, BRIGHT_RED, BRIGHT_GREEN, BOLD, GREY

# Set up console
console = Console()

# Redirect stdout and stderr to a file
log_file = 'output.log'
sys.stdout = open(log_file, 'w')
sys.stderr = open(log_file, 'w')

def get_user_input(prompt, default='s'):
    user_input = input(prompt).strip()
    if user_input == '':
        return default
    return user_input

# Example usage
run_type = get_user_input("How do you want to run 🗺️⁀જ✈︎ short/long:")

def run_subprocess(script_name, *args):
    subprocess.Popen(['python3', script_name] + list(args), stdout=subprocess.PIPE, stderr=subprocess.PIPE)

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

while True:
    try:
        peak = peak_time_handler()
        os.system('cls' if os.name == 'nt' else 'clear -x' if peak == 'NONPEAK' else 'clear')
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

    # Print and execute subprocesses
    print((BRIGHT_GREEN + UNDERLINE + "🏛 PXY® PreciseXceleratedYield Pvt Ltd™ 🏛".center(42) if mktpredict == 'RISE' else 
           BRIGHT_RED + UNDERLINE + "🏛 PXY® PreciseXceleratedYield Pvt Ltd™ 🏛".center(42) if mktpredict == 'FALL' else 
           BRIGHT_YELLOW + UNDERLINE + "🏛 PXY® PreciseXceleratedYield Pvt Ltd™ 🏛".center(42) if mktpredict == 'SIDE' else "")) + RESET)

    run_subprocess('cpritepxy.py')
    run_subprocess('tistpxy.py')
    run_subprocess('cntrloptpxy.py')
    run_subprocess('buyboptpxy.py')
    run_subprocess('buynoptpxy.py')
    
    if run_type == 's':
        run_subprocess('cntrloptprntpxy.py', 's')
    elif run_type == 'l':
        run_subprocess('cntrloptprntpxy.py', 'l')

    if run_type == 'l':
        run_subprocess('worldpxy.py')
        run_subprocess('buycncpxy.py') if peak == 'PEAKEND' and (mktpredict in ['RISE'] or Day_Change > 0 or Open_Change > 0) else None
        run_subprocess('niftychartpxy.py')
        run_subprocess('daypxy.py')
        run_subprocess('cndlpxy.py')
        print((BRIGHT_GREEN if nsma == "up" else BRIGHT_RED if nsma == "down" else BRIGHT_YELLOW) + "ﮩ٨ﮩ٨ـﮩ٨ﮩ٨ـﮩ٨ـﮩﮩ٨ﮩ٨NIFTY٨ﮩ٨ـﮩ٨ـﮩﮩ٨ﮩ٨ـﮩ٨ﮩ٨ـﮩ" + RESET)
        run_subprocess('bniftychartpxy.py')
        run_subprocess('bdaypxy.py')
        run_subprocess('bcndlpxy.py')
        print((BRIGHT_GREEN if bsma == "up" else BRIGHT_RED if bsma == "down" else BRIGHT_YELLOW) + "ﮩ٨ﮩ٨ـﮩ٨ﮩ٨ـﮩ٨ـﮩﮩ٨BANKNIFTY٨ﮩ٨ـﮩ٨ـﮩﮩ٨ﮩ٨ـﮩ٨ﮩ٨" + RESET)

    run_subprocess('cntrlcncpxy.py')

    print((BRIGHT_GREEN + UNDERLINE + "🏛 PXY® PreciseXceleratedYield Pvt Ltd™ 🏛".center(42) if mktpredict == 'RISE' else 
           BRIGHT_RED + UNDERLINE + "🏛 PXY® PreciseXceleratedYield Pvt Ltd™ 🏛".center(42) if mktpredict == 'FALL' else 
           BRIGHT_YELLOW + UNDERLINE + "🏛 PXY® PreciseXceleratedYield Pvt Ltd™ 🏛".center(42) if mktpredict == 'SIDE' else "")) + RESET

    run_subprocess('selfpxy.py')
    run_subprocess('plpxy.py')

    from sleeppxy import progress_bar
    from cyclepxy import cycle
    progress_bar(cycle, (mktpxy if peak in ["PEAKSART", "PEAKEND", "NONPEAK"] else None))

    # Wait for subprocesses to complete
    time.sleep(5)

    # Read and display log file content
    with open(log_file, 'r') as f:
        console.print(f.read())

    # Clear log file for next iteration
    open(log_file, 'w').close()

    # Wait before the next loop iteration
    time.sleep(60)  # Adjust as needed

