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
subprocess.run(['python3', 'cpritepxy.py'])
while True:
    from mktpxy import get_market_check
    importlib.reload(sys.modules['mktpxy'])  # Correct the usage
    onemincandlesequance, mktpxy = get_market_check('^NSEI')
    from nftpxy import nse_action, nse_power, Day_Change, Open_Change, OPTIONS
    importlib.reload(sys.modules['nftpxy'])  # Correct the usage
    from cyclepxy import cycle
    importlib.reload(sys.modules['cyclepxy'])  # Correct the usage
    from utcpxy import peak_time
    importlib.reload(sys.modules['utcpxy'])  # Correct the usage
    peak = peak_time()
    from macdpxy import calculate_macd_signal
    importlib.reload(sys.modules['macdpxy'])  # Correct the usage
    macd = calculate_macd_signal("^NSEI")
    from smapxy import check_index_status
    importlib.reload(sys.modules['smapxy'])  # Correct the usage
    nsma = check_index_status('^NSEI')
    ############################################"PXY® PreciseXceleratedYield Pvt Ltd™############################################
    subprocess.run(['python3', 'tistpxy.py'])
    subprocess.run(['python3', 'acvaluepxy.py']) if peak == 'PREPEAK' else None
    ############################################"PXY® PreciseXceleratedYield Pvt Ltd™############################################ 
    subprocess.run(['python3', 'cntrlcncpxy.py']) if peak == 'PEAKSTART' else None
    subprocess.run(['python3', 'cntrloptpxy.py']) if peak == 'PEAKSTART' else None
    subprocess.run(['python3', 'buyoptpxy.py']) if (nse_power > 0.9 and optpxy == 'Sell or Bear ') or (nse_power < 0.1 and optpxy == 'Buy or Bull') or peak == 'PEAKEND' else None
    subprocess.run(['python3', 'buycncpxy.py']) if (mktpxy == 'Buy' and Open_Change > 0) or peak == 'PEAKEND' else None
    ############################################"PXY® PreciseXceleratedYield Pvt Ltd™############################################ 
    subprocess.run(['python3', 'cntrlcncpxy.py']) 
    subprocess.run(['python3', 'cntrloptpxy.py']) 
    subprocess.run(['python3', 'cndlpxy.py'])
    from sleeppxy import progress_bar
    import time
    from rich.console import Console
    progress_bar(cycle, mktpxy)


