from bftpxy import get_bnk_action
from smapxy import check_index_status

def predict_bnk_sentiment():
    ha_nse_action, nse_power, Day_Change, Open_Change = get_bnk_action()
    sma = check_index_status('^NSEBANK')
    
    if Open_Change < 0 and sma == "down":
        bmktpredict = "FALL"
    elif Open_Change > 0 and sma == "up":
        bmktpredict = "RISE"
    else:
        bmktpredict = "SIDE"

    return bmktpredict
