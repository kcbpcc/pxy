import importlib
import subprocess
import os
from rich.console import Console
from clorpxy import RED, GREEN, SILVER, UNDERLINE, RESET, BRIGHT_YELLOW, BRIGHT_RED, BRIGHT_GREEN, BOLD, GREY

console = Console()

def get_user_input(prompt, default='s'):
    user_input = input(prompt).strip()
    return user_input if user_input else default

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
    importlib.reload(sys.modules['utcpxy'])
    return peak_time()

@handle_exceptions
def predict_market_sentiment_handler():
    from predictpxy import predict_market_sentiment
    importlib.reload(sys.modules['predictpxy'])
    return predict_market_sentiment()

@handle_exceptions
def get_market_check_handler(symbol):
    from mktpxy import get_market_check
    importlib.reload(sys.modules['mktpxy'])
    return get_market_check(symbol)

@handle_exceptions
def get_nse_action_handler():
    from nftpxy import get_nse_action
    importlib.reload(sys.modules['nftpxy'])
    return get_nse_action()

@handle_exceptions
def calculate_macd_signal_handler(symbol):
    from macdpxy import calculate_macd_signal
    return calculate_macd_signal(symbol)

@handle_exceptions
def check_index_status_handler(symbol):
    from smapxy import check_index_status
    return check_index_status(symbol)

def clear_console(peak):
    if os.name == 'nt':
        os.system('cls')
    else:
        if peak == 'NONPEAK':
            os.system('clear -x')

def print_mktpredict_message(mktpredict):
    if mktpredict == 'RISE':
        color = BRIGHT_GREEN
    elif mktpredict == 'FALL':
        color = BRIGHT_RED
    elif mktpredict == 'SIDE':
        color = BRIGHT_YELLOW
    else:
        color = ""
    print(f"{color + UNDERLINE + '🏛 PXY® PreciseXceleratedYield Pvt Ltd™ 🏛'.center(42) + RESET}")

def run_subprocess(command, condition=True):
    if condition:
        subprocess.run(command)

def main():
    while True:
        run_type = get_user_input("How do you want to run 🗺️⁀જ✈︎ short/long (Enter 'exit' to quit):")

        if run_type.lower() == 'exit':
            print("Exiting...")
            break
        
        subprocess.run(['python3', 'cpritepxy.py'])
        
        peak = peak_time_handler()
        clear_console(peak)
        
        mktpredict = predict_market_sentiment_handler()
        
        onemincandlesequance, mktpxy = get_market_check_handler('^NSEI')
        bnkonemincandlesequance, bmktpxy = get_market_check_handler('^NSEBANK')
        
        ha_nse_action, nse_power, Day_Change, Open_Change = get_nse_action_handler()
        
        macd = calculate_macd_signal_handler("^NSEI")
        nsma = check_index_status_handler('^NSEI')
        bsma = check_index_status_handler('^NSEBANK')
        
        print_mktpredict_message(mktpredict)
        
        run_subprocess(['python3', 'tistpxy.py'])
        run_subprocess(['python3', 'cntrloptpxy.py'] if run_type == 'l' else ['python3', 'cntrloptpxy.py', '-short'])
        
        if bmktpxy in ['Buy', 'Sell']:
            importlib.reload(sys.modules.get('mktpxy', None))
            print("━" * 42)
            subprocess.run(['python3', 'buyboptpxy.py'])
        
        if mktpxy in ['Buy', 'Sell']:
            importlib.reload(sys.modules.get('mktpxy', None))
            print("━" * 42)
            subprocess.run(['python3', 'buynoptpxy.py'])
        
        if run_type == 's':
            subprocess.run(['python3', 'mngoptpxy.py', 's'])
            subprocess.run(['python3', 'cntrloptprntpxy.py', 's'])
        elif run_type == 'l':
            subprocess.run(['python3', 'mngoptpxy.py', 'l'])
            subprocess.run(['python3', 'cntrloptprntpxy.py', 'l'])
        
        run_subprocess(['python3', 'worldpxy.py'] if run_type == 'l' else None)
        run_subprocess(['python3', 'buycncpxy.py'] if peak == 'PEAKEND' and (mktpredict in ['RISE'] or Day_Change > 0 or Open_Change > 0) else None)
        
        print_mktpredict_message(mktpredict)
        
        run_subprocess(['python3', 'niftychartpxy.py'] if run_type == 'l' else None)
        run_subprocess(['python3', 'daypxy.py'] if run_type == 'l' else None)
        run_subprocess(['python3', 'cndlpxy.py'] if run_type == 'l' else None)
        
        if run_type == 'l':
            color = BRIGHT_GREEN if nsma == "up" else BRIGHT_RED if nsma == "down" else BRIGHT_YELLOW
            print(f"{color + 'ﮩ٨ﮩ٨ـﮩ٨ﮩ٨ـﮩ٨ـﮩﮩ٨ﮩ٨NIFTY٨ﮩ٨ـﮩ٨ـﮩﮩ٨ﮩ٨ـﮩ٨ﮩ٨ـﮩ' + RESET}")
            
            run_subprocess(['python3', 'bniftychartpxy.py'])
            run_subprocess(['python3', 'bdaypxy.py'])
            run_subprocess(['python3', 'bcndlpxy.py'])
            
            color = BRIGHT_GREEN if bsma == "up" else BRIGHT_RED if bsma == "down" else BRIGHT_YELLOW
            print(f"{color + 'ﮩ٨ﮩ٨ـﮩ٨ﮩ٨ـﮩ٨ـﮩﮩ٨BANKNIFTY٨ﮩ٨ـﮩ٨ـﮩﮩ٨ﮩ٨ـﮩ٨ﮩ٨' + RESET}")
            
            run_subprocess(['python3', 'cntrlcncpxy.py'] if run_type == 'l' else ['python3', 'cntrlcncpxy.py', '-short']) if mktpredict in ['FALL', 'SIDE'] else None

        run_subprocess(['python3', 'selfpxy.py'])
        
        from sleeppxy import progress_bar
        from cyclepxy import cycle
        subprocess.run(['python3', 'plpxy.py'])
        progress_bar(cycle, (mktpxy if peak in ["PEAKSART", "PEAKEND", "NONPEAK"] else None))

if __name__ == "__main__":
    main()
