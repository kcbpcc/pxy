import subprocess
import os
from rich.console import Console
from clorpxy import BRIGHT_GREEN, BRIGHT_RED, RESET, UNDERLINE

def get_user_input(prompt, default='s'):
    return input(prompt).strip() or default

def run_script(script_name, *args):
    subprocess.run(['python3', script_name] + list(args), check=True)

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear -x')

def print_header(action):
    header = "🏛 PXY® PreciseXceleratedYield Pvt Ltd™ 🏛"
    color = {
        'Bullish': BRIGHT_GREEN,
        'Bearish': BRIGHT_RED
    }.get(action, RESET)
    print(color + header.center(42) + RESET)
    print("*" * 42)

def main():
    run_type = get_user_input("How do you want to run 🗺️⁀જ✈︎ short/long:")
    console = Console()

    # Execute initial script
    run_script('cpritepxy.py')

    # Handle peak time
    try:
        from utcpxy import peak_time
        peak = peak_time()
        clear_console()
    except Exception as e:
        print(f"Error handling peak time: {e}")
        peak = "NONPEAK"

    # Market sentiment prediction
    try:
        from predictpxy import predict_market_sentiment
        mktpredict = predict_market_sentiment()
    except Exception as e:
        print(f"Error handling market sentiment prediction: {e}")
        mktpredict = None

    # Get market check for NIFTY and BANKNIFTY
    try:
        from mktpxy import get_market_check
        onemincandlesequance, mktpxy = get_market_check('^NSEI')
        bnkonemincandlesequance, bmktpxy = get_market_check('^NSEBANK')
    except Exception as e:
        print(f"Error handling market check: {e}")
        onemincandlesequance, mktpxy = "none", "none"
        bnkonemincandlesequance, bmktpxy = "none", "none"

    # Get NSE action
    try:
        from nftpxy import get_nse_action
        ha_nse_action, nse_power, Day_Change, Open_Change = get_nse_action()
    except Exception as e:
        print(f"Error handling NSE action: {e}")
        ha_nse_action, nse_power, Day_Change, Open_Change = 0.5, 0.5, 0.5, 0.5

    # Calculate MACD signal
    try:
        from macdpxy import calculate_macd_signal
        macd = calculate_macd_signal("^NSEI")
    except Exception as e:
        print(f"Error handling MACD signal calculation: {e}")
        macd = None

    # Check index status
    try:
        from smapxy import check_index_status
        nsma = check_index_status('^NSEI')
        bsma = check_index_status('^NSEBANK')
    except Exception as e:
        print(f"Error handling index status: {e}")
        nsma, bsma = None, None

    # Print header
    print_header(ha_nse_action)

    # Execute main scripts based on conditions
    run_script('tistpxy.py')
    run_script('cntrloptpxy.py', '-short' if run_type == 's' else '')

    if peak == "PEAKSTART":
        run_script('telvalpxy.py')
    
    if bmktpxy in ['Buy', 'Sell']:
        print("━" * 42)
        run_script('buyboptpxy.py')
    else:
        print("━" * 42)
        print(f"{'Not Buying BANK opts ⛔ it is ' + bmktpxy + ' ⚠️':>41}")

    if mktpxy in ['Buy', 'Sell']:
        print("━" * 42)
        run_script('buynoptpxy.py')
    else:
        print("━" * 42)
        print(f"{'Not Buying NIFTY opts ⛔ it is ' + mktpxy + ' ⚠️':>41}")

    if run_type == 'l':
        run_script('niftychartpxy.py')
        run_script('daypxy.py')
        run_script('cndlpxy.py')
        if nsma:
            color = BRIGHT_GREEN if nsma == "up" else BRIGHT_RED if nsma == "down" else RESET
            print(color + "ﮩ٨ﮩ٨ـﮩ٨ﮩ٨ـﮩ٨ـﮩﮩ٨ﮩ٨NIFTY٨ﮩ٨ـﮩ٨ـﮩﮩ٨ﮩ٨ـﮩ٨ﮩ٨ـﮩ" + RESET)
        run_script('bniftychartpxy.py')
        run_script('bdaypxy.py')
        run_script('bcndlpxy.py')
        if bsma:
            color = BRIGHT_GREEN if bsma == "up" else BRIGHT_RED if bsma == "down" else RESET
            print(color + "ﮩ٨ﮩ٨ـﮩ٨ﮩ٨ـﮩ٨ـﮩﮩ٨BANKNIFTY٨ﮩ٨ـﮩ٨ـﮩﮩ٨ﮩ٨ـﮩ٨ﮩ٨ـﮩ" + RESET)

    print("━" * 42)
    if mktpredict in ['FALL', 'SIDE']:
        print(f"{UNDERLINE}{'💥💥  જ⁀➴ CNC Action - NIFTY on FALL  જ⁀➴':>38}{RESET}")
        run_script('cntrlcncpxy.py')
    else:
        print(f"{'✅ ✅ No Action - NIFTY on RISE  🆙 🆙':>38}")

    if peak == "PEAKEND":
        run_script('plpxy.py')

    print("━" * 42)
    run_script('selfpxy.py')

if __name__ == "__main__":
    main()
