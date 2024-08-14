from smapxy import calculate_sma50
ticker_symbol = '^NSEI'  # Replace with the actual ticker symbol
data = fetch_data(ticker_symbol)
sma_trend = calculate_sma50(data)
