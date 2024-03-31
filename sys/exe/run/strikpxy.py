import yfinance as yf
import warnings

# Suppress warnings
warnings.filterwarnings("ignore")

def get_50sma_price(symbol):
    data = yf.Ticker(symbol).history(period="1d", interval="1m")  # Fetch only one day of data
    price = data['Close'].rolling(window=50).mean()
    return price

def round_to_nearest_100(price):
    return round(price / 100) * 100

def round_to_nearest_100_or_50(price):
    # Apply rounding operation with handling NaN values
    rounded_price = price.apply(lambda x: round(x / 50) * 50 if x % 100 < 50 else round(x / 100) * 100)
    rounded_price = rounded_price.fillna(0)  # Replace NaN values with 0
    return rounded_price

def get_prices():
    noptions = round_to_nearest_100_or_50(get_50sma_price('^NSEI'))
    boptions = round_to_nearest_100(get_50sma_price('^NSEBANK'))  # Keep NSEBANK as nearest hundred only
    foptions = round_to_nearest_100_or_50(get_50sma_price('NIFTY_FIN_SERVICE.NS'))
    moptions = round_to_nearest_100_or_50(get_50sma_price('NIFTY_MID_SELECT.NS'))  # Fixed function call
    return noptions, boptions, foptions, moptions
