import warnings
import importlib
import subprocess
import time
import warnings
from rich.console import Console
console = Console()
warnings.simplefilter(action='ignore', category=FutureWarning)
import yfinance as yf
import pandas as pd
import colorama
from colorama import Fore, Style  # Add Style to the imports
from mktpxy import get_market_check
from nftpxy import nse_action, nse_power, Day_Change, Open_Change, OPTIONS
from utcpxy import peak_time
from macdpxy import calculate_macd_signal
from smapxy import check_index_status
import subprocess
import sys
onemincandlesequance, mktpxy = get_market_check("^NSEI")
peak = peak_time()
macd = calculate_macd_signal("^NSEI")
nsma = check_index_status("^NSEI")
from depthpxy import calculate_consecutive_candles
cedepth, pedepth = calculate_consecutive_candles("^NSEI")
colorama.init(autoreset=True)
nifty_data = yf.Ticker("^NSEI")
nifty_today = nifty_data.history(period='1d')
today_close = nifty_today['Close'].iloc[-1]
day_change_sign = '+' if Day_Change > 0 else ''
open_change_sign = '+' if Open_Change > 0 else ''
# Now you can use nifty50_ohlc outside of the function
print(f"🔆{day_change_sign}{Fore.GREEN if Day_Change >= 0 else Fore.RED}{Day_Change:.2f}{Style.RESET_ALL}⌛{open_change_sign}{Fore.GREEN if Open_Change >= 0 else Fore.RED}{Open_Change:.2f}{Style.RESET_ALL}⚡{Fore.GREEN if nse_power > 0.5 else Fore.RED}{nse_power:.2f}{Style.RESET_ALL}🟥-{pedepth}🚦📈:{int(today_close[0])}{macd}🚦{cedepth}+🟩")
