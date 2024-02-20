import yfinance as yf
import warnings

# Suppress warnings
warnings.filterwarnings("ignore")

def get_current_price(symbol):
    data = yf.Ticker(symbol).history(period="1d")
    return int(data['Close'].iloc[-1])

noptions = get_current_price('^NSEI')
boptions = get_current_price('^NSEBANK')
foptions = get_current_price('NIFTY_FIN_SERVICE.NS')
moptions = get_current_price('NIFTY_MIDCAP_100.NS')

print("Current price of Nifty:", noptions)
print("Current price of BankNifty:", boptions)
print("Current price of Nifty Financial Services:", foptions)
print("Current price of Nifty Midcap 100:", moptions)
