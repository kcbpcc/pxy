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
                consecutive_count = 1
                current_color = color

        # Calculate cedepth and pedepth
        if current_color is not None:
            if current_color == 'green':
                cedepth = consecutive_count
                pedepth = 1
            else:
                cedepth = 1
                pedepth = consecutive_count
                
            return cedepth, pedepth

    except Exception as e:
        return f"An error occurred: {e}"
