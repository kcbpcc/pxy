import yfinance as yf
import warnings

# Suppress warnings
warnings.filterwarnings("ignore")

# Define the ticker symbol
tickerSymbol = '^NSEI'

try:
    # Get data on this ticker
    tickerData = yf.Ticker(tickerSymbol)

    # Get the historical prices for this ticker
    tickerDf = tickerData.history(period='5d', interval='2m')

    # Calculate consecutive candles sequence
    consecutive_count = 1
    current_color = None

    for i in range(1, len(tickerDf)):
        if tickerDf['Close'][i] > tickerDf['Close'][i - 1]:
            color = 'green'
        elif tickerDf['Close'][i] < tickerDf['Close'][i - 1]:
            color = 'red'
        else:
            color = current_color

        if color == current_color:
            consecutive_count += 1
        else:
            if current_color is not None:
                if current_color == 'green':
                    print(f"The current state is +{consecutive_count}")
                else:
                    print(f"The current state is -{consecutive_count}")
            consecutive_count = 1
            current_color = color

    # Print the current state at the end
    if current_color is not None:
        if current_color == 'green':
            print(f"The current state is +{consecutive_count}")
        else:
            print(f"The current state is -{consecutive_count}")

except Exception as e:
    print(f"An error occurred: {e}")




