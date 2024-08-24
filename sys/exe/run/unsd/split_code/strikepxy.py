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

def get_strike(ticker_symbol):
    """
    Calculate four strike prices based on the current price of the given ticker symbol.
    """
    current_price = get_current_price(ticker_symbol)
    if current_price is not None:
        # Calculate PE and CE strike prices (rounded to nearest 100)
        bpprice = math.floor(current_price / 100) * 100
        spprice = bpprice + 100
        bcprice = math.ceil(current_price / 100) * 100
        scprice = bcprice + 100
        return bpprice, spprice, bcprice, scprice
    else:
        print("Current price is not available.")
        return None, None, None, None

def main():
    ticker_symbol = "^NSEI"  # Replace with the actual ticker symbol
    bpprice, spprice, bcprice, scprice = get_strike(ticker_symbol)
    if bpprice is not None and spprice is not None and bcprice is not None and scprice is not None:
        print(f"bpprice: {bpprice}")
        print(f"spprice: {spprice}")
        print(f"bcprice: {bcprice}")
        print(f"scprice: {scprice}")

if __name__ == "__main__":
    main()

