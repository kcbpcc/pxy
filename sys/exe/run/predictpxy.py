from nftpxy import get_nse_action
from smapxy import check_index_status
from clorpxy import BRIGHT_RED, BRIGHT_GREEN, BOLD, RESET

def predict_market_sentiment():
    ha_nse_action, nse_power, Day_Change, Open_Change = get_nse_action()
    nsma = check_index_status('^NSEI')
    Bearish = "Bearish"
    Bullish = "Bullish"

    if ha_nse_action == Bearish and nsma == "down":
        mktpredict = BRIGHT_RED + "FALLTREND" + RESET
    elif ha_nse_action == Bullish and nsma == "up":
        mktpredict = BRIGHT_GREEN + "RISETREND" + RESET
    else:
        mktpredict = BOLD + "SIDETREND" + RESET

    return mktpredict

# Call the function to predict market sentiment and print the result
predicted_sentiment = predict_market_sentiment()
