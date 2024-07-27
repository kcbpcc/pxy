from nftpxy import get_nse_action
from smapxy import check_index_status

def predict_market_sentiment(symbol):
    ha_nse_action, nse_power, Day_Change, Open_Change = get_nse_action()
    nsma = check_index_status(symbol)
    Bearish = "Bearish"
    Bullish = "Bullish"

    if ha_nse_action == Bearish and nsma == "down":
        mktpredict = "FALL"
    elif ha_nse_action == Bullish and nsma == "up":
        mktpredict = "RISE"
    else:
        mktpredict = "SIDE"

    return mktpredict

# Example usage:
#symbol = '^NSEI'  # Replace with any symbol you want
#predicted_sentiment = predict_market_sentiment(symbol)
#print(predicted_sentiment)
