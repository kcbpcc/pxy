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
        consecutive_count = 0
        cedepth = 0
        pedepth = 0

        for i in range(1, len(tickerDf)):
            if tickerDf['Close'][i] > tickerDf['Close'][i - 1]:
                consecutive_count += 1
            elif tickerDf['Close'][i] < tickerDf['Close'][i - 1]:
                consecutive_count = 0

            if consecutive_count == 9:  # Reached 9 consecutive candles
                if tickerDf['Close'][i] > tickerDf['Close'][i - 1]:  # Next candle is green
                    cedepth = 9
                    pedepth = 0
                elif tickerDf['Close'][i] < tickerDf['Close'][i - 1]:  # Next candle is red
                    cedepth = 8
                    pedepth = 1
                break

        return cedepth, pedepth

    except Exception as e:
        return f"An error occurred: {e}"
