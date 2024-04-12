# Importing required modules
from nftpxy import get_nse_action
from smapxy import check_index_status
from clorpxy import SILVER, UNDERLINE, RED, GREEN, YELLOW, RESET, BRIGHT_YELLOW, BRIGHT_RED, BRIGHT_GREEN, BOLD, GREY

# Getting data
ha_nse_action, nse_power, Day_Change, Open_Change = get_nse_action()
nsma = check_index_status('^NSEI')

# Defining variables
Bearish = "Bearish"
Bullish = "Bullish"

# Predicting market sentiment
if ha_nse_action == Bearish and nsma == "down":
    predictmkt = BRIGHT_RED + "hopeless" + RESET
elif ha_nse_action == Bullish and nsma == "up":
    predictmkt = BRIGHT_GREEN + "hopeful" + RESET
else:
    predictmkt = BOLD + "useless" + RESET

print("Predicted market sentiment:", predictmkt)
