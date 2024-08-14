from yfdata import fetch_data
from ashi import calculate_heikin_ashi

def calculate_candle_sequence(ha_close, ha_open):
    """Generate a sequence of candle colors based on Heikin-Ashi data."""
    return ''.join(['🟩' if ha_close.iloc[-i] > ha_open.iloc[-i] else '🟥' for i in range(1, 4)][::-1])

def get_market_signal(current_color, last_closed_color):
    """Determine the market signal."""
    if current_color == 'Bear' and last_closed_color == 'Bear':
        return 'Bear'
    elif current_color == 'Bull' and last_closed_color == 'Bull':
        return 'Bull'
    elif current_color == 'Bear' and last_closed_color == 'Bull':
        return 'Sell'
    elif current_color == 'Bull' and last_closed_color == 'Bear':
        return 'Buy'
    else:
        return 'None'

def get_market_check(symbol):
    """Get market sentiment based on Heikin-Ashi candle colors."""
    data = fetch_data(symbol)
    if data is None or data.empty:
        return "", "None"

    ha_close, ha_open = calculate_heikin_ashi(data)
    candle_sequence = calculate_candle_sequence(ha_close, ha_open)

    current_color = 'Bear' if ha_close.iloc[-1] < ha_open.iloc[-1] else 'Bull'
    last_closed_color = 'Bear' if ha_close.iloc[-2] < ha_open.iloc[-2] else 'Bull'

    market_signal = get_market_signal(current_color, last_closed_color)
    return candle_sequence, market_signal
