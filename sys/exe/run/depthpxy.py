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
        consecutive_count = 1
        current_color = None
        cedepth = 0
        pedepth = 0

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
                if current_color == 'green':
                    cedepth += min(consecutive_count, 10 - pedepth)
                elif current_color == 'red':
                    pedepth += min(consecutive_count, 10 - cedepth)
                consecutive_count = 1
                current_color = color

        # Add the last segment to depths
        if current_color is not None:
            if current_color == 'green':
                cedepth += min(consecutive_count, 10 - pedepth)
            else:
                pedepth += min(consecutive_count, 10 - cedepth)

        return cedepth, pedepth

    except Exception as e:
        return f"An error occurred: {e}"
