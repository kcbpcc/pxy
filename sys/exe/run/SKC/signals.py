from check import get_market_check

def print_market_signals(ticker_symbol):
    """Print the market signals for the specified ticker symbol."""
    candle_sequence, market_signal = get_market_check(ticker_symbol)
    print(f"Candle Sequence: {candle_sequence}")
    print(f"Market Signal: {market_signal}")
