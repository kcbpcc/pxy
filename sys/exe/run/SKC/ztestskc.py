# calculate_consecutive_candles.py
import yfinance as yf
import pandas as pd

def calculate_consecutive_candles(ticker_symbol):
    try:
        # Get data on this ticker
        ticker_data = yf.Ticker(ticker_symbol)
        ticker_df = ticker_data.history(period='5d', interval='1m')

        # Calculate Heikin-Ashi candles
        ha_close = (ticker_df['Open'] + ticker_df['High'] + ticker_df['Low'] + ticker_df['Close']) / 4
        ha_open = ha_close.shift(1)
        ha_color = pd.Series('green', index=ha_close.index)
        ha_color[ha_close < ha_open] = 'red'

        # Calculate consecutive candles sequence
        consecutive_count = 1
        current_color = ha_color.iloc[-1]

        for i in range(1, len(ha_color)):
            if ha_color.iloc[i] == ha_color.iloc[i - 1]:
                consecutive_count += 1
            else:
                consecutive_count = 1
                current_color = ha_color.iloc[i]

        # Calculate cedepth and pedepth
        if current_color == 'green':
            cedepth = min(consecutive_count, 9)
            pedepth = 1
        else:
            cedepth = 1
            pedepth = min(consecutive_count, 9)

        # Format depth values with signs
        cedepth_str = f"+{cedepth}" if cedepth > 0 else f"{cedepth}"
        pedepth_str = f"+{pedepth}" if pedepth > 0 else f"{pedepth}"

        return cedepth_str, pedepth_str
    except Exception as e:
        return f"An error occurred: {e}"

def main():
    ticker_symbol = '^NSEI'  # Replace with the actual ticker symbol
    cedepth, pedepth = calculate_consecutive_candles(ticker_symbol)
    
    # Print depth values
    print(f"cedepth = {cedepth}")
    print(f"pedepth = {pedepth}")

if __name__ == "__main__":
    main()
