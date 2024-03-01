import yfinance as yf
import warnings

# Suppress warnings
warnings.filterwarnings("ignore")

def get_current_price(symbol):
    data = yf.Ticker(symbol).history(period="2d", interval="1m")

    price = data.iloc[-1]  # Fixed missing assignment of last_row

    return price  # Added return statement

def round_to_nearest_100(price):
    return round(price / 100) * 100

def round_to_nearest_100_or_50(price):
    return round(price / 50) * 50 if price % 100 < 50 else round(price / 100) * 100

def get_prices():
    noptions = round_to_nearest_100_or_50(get_current_price('^NSEI'))
    boptions = round_to_nearest_100(get_current_price('^NSEBANK'))
    foptions = round_to_nearest_100_or_50(get_current_price('NIFTY_FIN_SERVICE.NS'))
    moptions = round_to_nearest_100_or_50(get_current_price('NIFTY_MID_SELECT.NS'))
    return noptions, boptions, foptions, moptions

