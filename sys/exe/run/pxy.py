import subprocess
import time
import importlib
import sys
import os
from rich.console import Console
from cyclepxy import cycle
from sleeppxy import progress_bar
from predictpxy import predict_market_sentiment
from mktpxy import get_market_check
from nftpxy import get_nse_action
from utcpxy import peak_time
from macdpxy import calculate_macd_signal
from smapxy import check_index_status

console = Console()

def main():
    # Open the output file in append mode
    with open('pxy.log', 'a') as output_file:
        subprocess.run(['python3', 'cpritepxy.py'])
        while True:
            importlib.reload(sys.modules['predictpxy'])
            mktpredict = predict_market_sentiment()
            
            importlib.reload(sys.modules['mktpxy'])
            onemincandlesequance, mktpxy = get_market_check('^NSEI')
            
            importlib.reload(sys.modules['nftpxy'])
            ha_nse_action, nse_power, Day_Change, Open_Change = get_nse_action()
            
            importlib.reload(sys.modules['cyclepxy'])
            peak = peak_time()
            
            importlib.reload(sys.modules['macdpxy'])
            macd = calculate_macd_signal("^NSEI")
            
            importlib.reload(sys.modules['smapxy'])
            nsma = check_index_status('^NSEI')
            
            subprocess.run(['python3', 'acvaluepxy.py']) if peak == 'PREPEAK' else None
            subprocess.run(['python3', 'worldpxy.py'])
            subprocess.run(['python3', 'buyoptpxy.py'])
            subprocess.run(['python3', 'buycncpxy.py']) if (not (Open_Change < 0 and Day_Change < 0 and nsma == 'down') and mktpxy == 'Buy') or peak == 'PEAKEND' else None
            subprocess.run(['python3', 'cntrlcncpxy.py'])
            subprocess.run(['python3', 'cntrloptpxy.py'])
            subprocess.run(['python3', 'cndlpxy.py'])
            subprocess.run(['python3', 'selfpxy.py'])
            subprocess.run(['python3', 'daypxy.py'])
            
            # Print the predicted market sentiment
            console.print(f"    PXY® Predicted market sentiment : {mktpredict}")
            
            # Write the output to the log file
            output_file.write(f"PXY® Predicted market sentiment : {mktpredict}\n")
            output_file.flush()  # Ensure the data is written immediately
            
            # Display progress bar
            progress_bar(cycle, mktpxy)
            
            # Clear the screen
            os.system('clear')

            time.sleep(1)  # Adjust the sleep time according to your needs

if __name__ == "__main__":
    main()

