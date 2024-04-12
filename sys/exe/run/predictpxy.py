# Importing required modules
from nftpxy import get_nse_action
from smapxy import check_index_status

# Getting data
ha_nse_action, nse_power, Day_Change, Open_Change = get_nse_action()
nsma = check_index_status('^NSEI')

# Defining variables
Bearish = "Bearish"
Bullish = "Bullish"

# Predicting market sentiment
if ha_nse_action == Bearish and nsma == "down":
    predictmkt = "hopeless"
elif ha_nse_action == Bullish and nsma == "up":
    predictmkt = "hopeful"
else:
    predictmkt = "can't say"

# Printing the predicted market sentiment
print("Predicted market sentiment:", predictmkt)
