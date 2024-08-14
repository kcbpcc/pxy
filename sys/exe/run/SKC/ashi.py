def calculate_heikin_ashi(data):
    """Calculate Heikin-Ashi values."""
    ha_close = (data['Open'] + data['High'] + data['Low'] + data['Close']) / 4
    ha_open = (data['Open'].shift(1) + data['Close'].shift(1)) / 2
    return ha_close, ha_open

def get_heikin_ashi_action(ha_close, ha_open):
    """Determine the Heikin-Ashi action."""
    return "Bullish" if ha_close.iloc[-1] > ha_open.iloc[-1] else "Bearish"
