import yfinance as yf
import math

def get_nifty50_current_price():
    ticker_symbol = "^NSEI"  # NIFTY50 index symbol on Yahoo Finance
    try:
        nifty_data = yf.Ticker(ticker_symbol).history(period="1d")
        current_price = nifty_data['Close'].iloc[-1]
        return current_price
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

def calculate_strikes(current_price):
    if current_price is not None:
        # Calculate PE strike price (current price - 500, rounded to nearest 500)
        pprice = math.floor((current_price - 0) / 100) * 100
        # Calculate CE strike price (current price + 500, rounded to nearest 500)
        cprice = math.ceil((current_price + 0) / 100) * 100
        return pprice, cprice
    else:
        print("Current price is not available.")
        return None, None

def main():
    current_price = get_nifty50_current_price()
    pprice, cprice = calculate_strikes(current_price)
    if pprice is not None and cprice is not None:
        print(f"pprice: {pprice}")
        print(f"cprice: {cprice}")

if __name__ == "__main__":
    main()
