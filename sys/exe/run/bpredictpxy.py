from bftpxy import get_bnk_action
from smapxy import check_index_status

def predict_bmarket_sentiment():
    ha_nse_action, nse_power, Day_Change, Open_Change = get_nse_action()
    nsma = check_index_status('^NSEBANK')
    Bearish = "Bearish"
    Bullish = "Bullish"

    if ha_nse_action == Bearish and nsma == "down":
        mktpredict = "FALL"
    elif ha_nse_action == Bullish and nsma == "up":
        mktpredict = "RISE"
    else:
        mktpredict = "SIDE"

    return mktpredict

# Call the function to predict market sentiment and print the result
predicted_sentiment = predict_market_sentiment()
#print(predicted_sentiment)
