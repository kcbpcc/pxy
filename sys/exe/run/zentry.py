import pandas as pd
import requests

def get_candlestick_pattern(symbol):
    exchange_code = ".NS"  # Replace with the appropriate exchange code for your symbols

    # Append the exchange code to the symbol
    full_symbol = f"{symbol}{exchange_code}"

    # Replace this URL with the appropriate Yahoo Finance API URL for historical data
    url = f'https://query1.finance.yahoo.com/v8/finance/chart/{full_symbol}?interval=1d'

    try:
        response = requests.get(url)
        data = response.json()

        # Extract candlestick pattern from the response data
        # You may need to adjust this based on the actual structure of the Yahoo Finance API response
        # For simplicity, let's assume that a "bearish" candlestick pattern is when the close is lower than the open
        close = data['chart']['result'][0]['indicators']['quote'][0]['close']
        open_ = data['chart']['result'][0]['indicators']['quote'][0]['open']

        if close[-1] < open_[-1]:
            return "Bearish"
        else:
            return "Bullish"

    except Exception as e:
        print(f"Error fetching data for {full_symbol}: {e}")
        return None

def main():
    # Load the CSV file into a pandas DataFrame
    df = pd.read_csv('yxplist.csv')

    # Iterate over each row in the DataFrame
    for index, row in df.iterrows():
        symbol = row['tradingsymbol']
        candlestick_pattern = get_candlestick_pattern(symbol)

        if candlestick_pattern:
            print(f"{symbol}: {candlestick_pattern} trend")

if __name__ == "__main__":
    main()





