import yfinance as yf
import warnings

# Suppress warnings
warnings.filterwarnings("ignore")

def get_current_price(symbol):
    data = yf.Ticker(symbol).history(period="1d")
    return int(data['Close'].iloc[-1])

def get_prices():
    noptions = get_current_price('^NSEI')
    boptions = get_current_price('^NSEBANK')
    foptions = get_current_price('NIFTY_FIN_SERVICE.NS')
    moptions = get_current_price('NIFTY_MIDCAP_100.NS')
    return noptions, boptions, foptions, moptions
