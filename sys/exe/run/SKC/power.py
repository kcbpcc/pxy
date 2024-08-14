def calculate_stock_power(current_price, today_low, today_high):
    """Calculate stock power based on current price, today's low, and high."""
    raw_stock_power = (current_price - (today_low - 0.01)) / (abs(today_high + 0.01) - abs(today_low - 0.01))
    stock_power = round(max(0.1, min(raw_stock_power, 1.0)), 2)
    return stock_power
