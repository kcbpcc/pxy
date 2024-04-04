import yfinance as yf
import warnings

def calculate_consecutive_candles(tickerSymbol):
    # Suppress warnings
    warnings.filterwarnings("ignore")

    try:
        # Get data on this ticker
        tickerData = yf.Ticker(tickerSymbol)

        # Get the historical prices for this ticker
        tickerDf = tickerData.history(period='5d', interval='1m')

        # Calculate consecutive candles sequence
        consecutive_counts = []

        for i in range(1, len(tickerDf)):
            if tickerDf['Close'][i] > tickerDf['Close'][i - 1]:
                color = 'green'
            elif tickerDf['Close'][i] < tickerDf['Close'][i - 1]:
                color = 'red'
            else:
                color = None

            # Append current color to the consecutive counts history
            consecutive_counts.append(color)

            # Keep only the last 10 entries in the history
            if len(consecutive_counts) > 10:
                consecutive_counts.pop(0)

            # Count consecutive candles from the history
            consecutive_green = consecutive_counts.count('green')
            consecutive_red = consecutive_counts.count('red')

            # Calculate cedepth and pedepth
            cedepth = min(consecutive_green, 10)
            pedepth = min(consecutive_red, 10 - cedepth)

            # Return the counts if we have at least 9 candles
            if len(consecutive_counts) >= 9:
                return cedepth, pedepth

    except Exception as e:
        return f"An error occurred: {e}"

# Example usage
cedepth, pedepth = calculate_consecutive_candles("AAPL")
print("CE Depth:", cedepth)
print("PE Depth:", pedepth)

