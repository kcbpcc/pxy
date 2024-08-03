import yfinance as yf

def get_strike_prices(nifty_ticker='^NSEI', banknifty_ticker='NSEBANK'):
    """
    Fetches the latest closing prices for Nifty and Bank Nifty and calculates their rounded strike prices.
    
    Args:
        nifty_ticker (str): Ticker symbol for Nifty.
        banknifty_ticker (str): Ticker symbol for Bank Nifty.

    Returns:
        tuple: A tuple containing rounded strike prices for Nifty and Bank Nifty.
    """
    # Fetch the data
    nifty_data = yf.Ticker(nifty_ticker).history(period="1d", interval="1m")
    banknifty_data = yf.Ticker(banknifty_ticker).history(period="1d", interval="1m")
    
    # Initialize the strike prices
    Nstrike = None
    Bstrike = None

    # Extract the latest closing price and round to the nearest 100
    if not nifty_data.empty:
        nifty_close = nifty_data['Close'].iloc[-1]
        Nstrike = round(nifty_close / 100) * 100
    
    if not banknifty_data.empty:
        banknifty_close = banknifty_data['Close'].iloc[-1]
        Bstrike = round(banknifty_close / 100) * 100

    return Nstrike, Bstrike

# Example usage
nifty_strike, banknifty_strike = get_strike_prices()
print(f"Nifty strike price: {nifty_strike}")
print(f"Bank Nifty strike price: {banknifty_strike}")
