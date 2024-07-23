import yfinance as yf

def get_vixpxy(nifty_symbol='^NSEI', bank_nifty_symbol='^NSEBANK'):
    # Fetch historical 1-minute data for the last 5 days for Nifty
    nifty_data = yf.Ticker(nifty_symbol).history(period="5d", interval="1m")
    # Fetch historical 1-minute data for the last 5 days for Bank Nifty
    bank_nifty_data = yf.Ticker(bank_nifty_symbol).history(period="5d", interval="1m")

    # Initialize results
    nvix = 1
    bvix = 1

    # Calculate Nifty absolute difference if data is fetched
    if not nifty_data.empty:
        nifty_data['SMA50'] = nifty_data['Close'].rolling(window=50).mean()
        latest_nifty_data = nifty_data.iloc[-1]
        nifty_price = latest_nifty_data['Close']
        sma50_nifty_price = latest_nifty_data['SMA50']
        nvix = abs(nifty_price - sma50_nifty_price) / 10

    # Calculate Bank Nifty absolute difference if data is fetched
    if not bank_nifty_data.empty:
        bank_nifty_data['SMA50'] = bank_nifty_data['Close'].rolling(window=50).mean()
        latest_bank_nifty_data = bank_nifty_data.iloc[-1]
        bank_nifty_price = latest_bank_nifty_data['Close']
        sma50_bank_nifty_price = latest_bank_nifty_data['SMA50']
        bvix = abs(bank_nifty_price - sma50_bank_nifty_price) / 20

    # Return the values as a tuple
    return nvix, bvix
