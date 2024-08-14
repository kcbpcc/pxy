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
        pe_strike = math.floor((current_price - 500) / 500) * 500
        # Calculate CE strike price (current price + 500, rounded to nearest 500)
        ce_strike = math.ceil((current_price + 500) / 500) * 500
        return pe_strike, ce_strike
    else:
        print("Current price is not available.")
        return None, None

def main():
    current_price = get_nifty50_current_price()
    pe_strike, ce_strike = calculate_strikes(current_price)
    if pe_strike is not None and ce_strike is not None:
        print(f"PE Strike Price: {pe_strike}")
        print(f"CE Strike Price: {ce_strike}")

if __name__ == "__main__":
    main()
