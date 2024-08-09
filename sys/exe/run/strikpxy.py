import yfinance as yf
import warnings

# Suppress warnings
warnings.filterwarnings("ignore")

def get_current_price(symbol):
    data = yf.Ticker(symbol).history(period="1d", interval="1m")  # Fetch only one day of data
    current_price = data['Close'].iloc[-1]  # Get the last available price
    return current_price

def round_to_nearest_500(price):
    return round(price / 500) * 500

def round_to_nearest_1000(price):
    return round(price / 1000) * 1000

def get_prices():
    BCE_Strike = round_to_nearest_1000(get_current_price('^NSEBANK'))
    CE_Strike = round_to_nearest_500(get_current_price('^NSEI'))
    PE_Strike = round_to_nearest_500(get_current_price('^NSEI'))
    BPE_Strike = round_to_nearest_1000(get_current_price('^NSEBANK'))
                                    
    return BCE_Strike, CE_Strike, PE_Strike, BPE_Strike


