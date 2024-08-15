import yfinance as yf
import math

def get_current_price(ticker_symbol):
    """
    Fetch the current price for the given ticker symbol.
    """
    try:
        data = yf.Ticker(ticker_symbol).history(period="1d")
        current_price = data['Close'].iloc[-1]
        return current_price
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

def calculate_strikes(ticker_symbol):
    """
    Calculate PE and CE strike prices based on the current price of the given ticker symbol.
    """
    current_price = get_current_price(ticker_symbol)
    if current_price is not None:
        # Calculate PE strike price (rounded to nearest 100 below)
        bpprice = math.floor((current_price - 0) / 100) * 100
        spprice = math.floor((current_price - 0) / 100) * 100 +100
        # Calculate CE strike price (rounded to nearest 100 above)
        bcprice = math.ceil((current_price + 0) / 100) * 100
        scprice = math.ceil((current_price + 0) / 100) * 100 + 100
        return pprice, cprice
    else:
        print("Current price is not available.")
        return None, None

def main():
    ticker_symbol = "^NSEI"  # Replace with the actual ticker symbol
    pprice, cprice = calculate_strikes(ticker_symbol)
    if pprice is not None and cprice is not None:
        print(f"pprice: {pprice}")
        print(f"cprice: {cprice}")

if __name__ == "__main__":
    main()
