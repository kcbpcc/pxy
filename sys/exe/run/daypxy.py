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
from nftpxy import nse_action, nse_power, Day_Change, Open_Change, OPTIONS

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
today_close = nifty_today['Close'].iloc[-1]

day_change_sign = '+' if Day_Change > 0 else ''
open_change_sign = '+' if Open_Change > 0 else ''

print(f"🔆{day_change_sign}{Fore.GREEN if Day_Change >= 0 else Fore.RED}{Day_Change:.2f}{Style.RESET_ALL}"
      f"⌛{open_change_sign}{Fore.GREEN if Open_Change >= 0 else Fore.RED}{Open_Change:.2f}{Style.RESET_ALL}"
      f"⚡{Fore.GREEN if nse_power > 0.5 else Fore.RED}{nse_power:.2f}{Style.RESET_ALL}"
      f"🟥-{pedepth}🚦📈:{int(today_close[0])}{macd}🚦{cedepth}+🟩")
