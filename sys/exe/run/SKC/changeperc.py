def calculate_percentage_change(current_value, previous_value):
    """Calculate percentage change between current and previous values."""
    if previous_value == 0:  # Avoid division by zero
        return 0.0
    return round(((current_value - previous_value) / previous_value) * 100, 2)
