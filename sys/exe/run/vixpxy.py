import yfinance as yf

def get_vix_data(ticker):
    vix = yf.Ticker(ticker)
    data = vix.history(period="1d")  # Fetch historical data for 1 day
    return data

def main():
    # Ticker for India VIX
    india_vix_ticker = "^INDIAVIX"

    # Fetch VIX data
    vix_data = get_vix_data(india_vix_ticker)

    # Display the most recent data
    print("India VIX Data:")
    print(vix_data.tail())

if __name__ == "__main__":
    main()
