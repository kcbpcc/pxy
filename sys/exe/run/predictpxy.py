from nftpxy import get_nse_action
from smapxy import check_index_status

def predict_market_sentiment():
    ha_nse_action, nse_power, Day_Change, Open_Change = get_nse_action()
    sma = check_index_status('^NSEI')

    if Open_Change < 0 and sma == "down":
        mktpredict = "FALL"
    elif Open_Change > 0 and sma == "up":
        mktpredict = "RISE"
    else:
        mktpredict = "SIDE"

    return mktpredict
