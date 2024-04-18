delta = 200
import yfinance as yf
import warnings
from datetime import datetime, timedelta

# Suppress warnings
warnings.filterwarnings("ignore")

def get_current_price(symbol):
    data = yf.Ticker(symbol).history(period="1d", interval="1m")  # Fetch only one day of data
    current_price = data['Close'].iloc[-1]  # Get the last available price
    return current_price

def round_to_nearest_100(price):
    return round(price / 100) * 100

def round_to_nearest_100_or_50(price):
    return round(price / 50) * 50 if price % 100 < 50 else round(price / 100) * 100

today = datetime.now()
days_left_until_thursday = 4 #(3 - today.weekday()) % 7  # Thursday is weekday 3
#print("Days remaining until Thursday:", days_left_until_thursday)    

def get_prices():
    noptions = round_to_nearest_100(get_current_price('^NSEI'))
    CE_Strike = round_to_nearest_100(get_current_price('^NSEI'))
    PE_Strike = round_to_nearest_100(get_current_price('^NSEI')) + 200
    dummy = round_to_nearest_100(get_current_price('^NSEI')) 
                                    
    return noptions, CE_Strike, PE_Strike, dummy
    print("CE_Strike:", CE_Strike, "PE_Strike:", PE_Strike)
#print(get_prices())

