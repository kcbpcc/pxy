import yfinance as yf
import warnings

def calculate_consecutive_candles(tickerSymbol):
    # Suppress warnings
    warnings.filterwarnings("ignore")

    try:
        # Get data on this ticker
        tickerData = yf.Ticker(tickerSymbol)

        # Get the historical prices for this ticker
        tickerDf = tickerData.history(period='10d', interval='5m')

        # Limit the analysis to the latest 10 candles
        latest_data = tickerDf.tail(10)

        # Calculate consecutive candles sequence
        consecutive_count = 1
        current_color = None
        latest_pattern = []

        for i in range(1, len(latest_data)):
            if latest_data['Close'][i] > latest_data['Close'][i - 1]:
                color = 'green'
            elif latest_data['Close'][i] < latest_data['Close'][i - 1]:
                color = 'red'
            else:
                color = current_color

            if color == current_color:
                consecutive_count += 1
            else:
                if current_color is not None:
                    latest_pattern.append((current_color, consecutive_count))
                consecutive_count = 1
                current_color = color

        # Add the last pattern
        if current_color is not None:
            latest_pattern.append((current_color, consecutive_count))

        # Display the latest two patterns
        if len(latest_pattern) >= 2:
            latest_two_patterns = latest_pattern[-2:]
            return latest_two_patterns

    except Exception as e:
        return f"An error occurred: {e}"

# Example usage:
latest_patterns = calculate_consecutive_candles("AAPL")
if latest_patterns:
    for pattern in latest_patterns:
        color, count = pattern
        print(f"{count} {color} ", end="")
    print()
else:
    print("No patterns found.")
