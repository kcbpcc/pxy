from nftpxy import get_nse_action
from smapxy import check_index_status
from clorpxy import SILVER, UNDERLINE, RED, GREEN, YELLOW, RESET, BRIGHT_YELLOW, BRIGHT_RED, BRIGHT_GREEN, BOLD, GREY
ha_nse_action, nse_power, Day_Change, Open_Change = get_nse_action()
nsma = check_index_status('^NSEI')
Bearish = "Bearish"
Bullish = "Bullish"
if ha_nse_action == Bearish and nsma == "down":
    predictmkt = BRIGHT_RED + "hopeless" + RESET
elif ha_nse_action == Bullish and nsma == "up":
    predictmkt = BRIGHT_GREEN + "hopeful" + RESET
else:
    predictmkt = BOLD + "useless" + RESET
print("Predicted market sentiment:", predictmkt)
return predictmkt
