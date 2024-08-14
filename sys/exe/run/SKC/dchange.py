from changeperc import calculate_percentage_change
from yfdata import fetch_data

def get_day_change(ticker):
    """Get the day change percentage for the given ticker."""
    data = fetch_data(ticker)
    if data is None or data.empty:
        return None, None  # Return None for both values
    
    current_price = data['Close'].iloc[-1]
    yesterday_close = data['Close'].iloc[-2]
    day_change_value = calculate_percentage_change(current_price, yesterday_close)
    return day_change_value, current_price, yesterday_close
