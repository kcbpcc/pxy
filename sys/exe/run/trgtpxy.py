# trgtpxy.py

def calculate_trgtpxy(nse_power):
    if 0.90 <= nse_power <= 1.0:
        return 9.0
    elif 0.75 <= nse_power < 0.90:
        return 7.0
    elif 0.5 <= nse_power < 0.75:
        return 5.0
    elif 0.3 <= nse_power < 0.50:
        return 3.0
    elif 0.0 <= nse_power < 0.25:
        return 1.0
    else:
        return 5.0  # Default value if none of the conditions are met


