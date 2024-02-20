import yfinance as yf

# Define the symbols
symbols = ['^NSEI', '^NSEBANK', 'NIFTY_FIN_SERVICE.NS', 'NIFTY_MIDCAP_100.NS']

# Function to get current price with no decimals
def get_current_prices(symbol):
    data = yf.Ticker(symbol).history(period="1d")
    current_price = int(data['Close'].iloc[-1])
    return current_price, current_price * 0.1, current_price * 0.2, current_price * 0.3

# Get and print current prices
for symbol in symbols:
    options, boptions, foptions, moptions = get_current_prices(symbol)
    print(f"Symbol: {symbol}, Options: {options}, BOptions: {boptions}, FOptions: {foptions}, MOptions: {moptions}")
