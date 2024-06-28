import time
import warnings
from rich.console import Console
import yfinance as yf
import pandas as pd
import colorama
from colorama import Fore, Style
from mktpxy import get_market_check
from utcpxy import peak_time
from macdpxy import calculate_macd_signal
from smapxy import check_index_status
from depthpxy import calculate_consecutive_candles
from nftpxy import get_nse_action
ha_nse_action, nse_power, Day_Change, Open_Change  = get_nse_action()

console = Console()
warnings.simplefilter(action='ignore', category=FutureWarning)
colorama.init(autoreset=True)

onemincandlesequance, mktpxy = get_market_check("^NSEI")
peak = peak_time()
macd = calculate_macd_signal("^NSEI")
nsma = check_index_status("^NSEI")
cedepth, pedepth = calculate_consecutive_candles("^NSEI")

nifty_data = yf.Ticker("^NSEI")
nifty_today = nifty_data.history(period='1d')

try:
    current_price = nifty_today['Close'].iloc[-1]  # Assuming 'Close' column represents the current price
except IndexError:
    print("Error: Unable to retrieve today's current price.")
    exit(1)

if current_price is None:
    print("Error: 'current_price' is None.")
    exit(1)

day_change_sign = '+' if Day_Change > 0 else ''
open_change_sign = '+' if Open_Change > 0 else ''

def emoimktpxy(mktpxy):
    emojis = {
        'buy': '👆',
        'bull': '👉',
        'sell': '👇',
        'bear': '👈',
        'none': '✊'
    }
    return emojis.get(mktpxy.lower(), '❓')
emojipxy = emoimktpxy(mktpxy)

print(f"🟥-{pedepth}🔆{day_change_sign}{Fore.GREEN if Day_Change >= 0 else Fore.RED}{Day_Change:.2f}{Style.RESET_ALL}⌛{open_change_sign}{Fore.GREEN if Open_Change >= 0 else Fore.RED}{Open_Change:.2f}{Style.RESET_ALL}⚡{Fore.GREEN if nse_power > 0.5 else Fore.RED}{nse_power:.2f}{Style.RESET_ALL}NF:{int(current_price)}🚦{emojipxy}🚦{cedepth}+🟩")

