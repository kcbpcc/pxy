from changeperc import calculate_percentage_change
from yfdata import fetch_data

def get_open_change(ticker):
    """Get the open change percentage for the given ticker."""
    data = fetch_data(ticker)
    if data is None or data.empty:
        return None, None  # Return None for both values
    
    today_open = data['Open'].iloc[-1]
    current_price = data['Close'].iloc[-1]
    open_change_value = calculate_percentage_change(current_price, today_open)
    return open_change_value, today_open, current_price
