# trgtpxy.py

def calculate_trgtpxy(timpxy, nse_action):
    if nse_action == "Bullish":
        return round(float(timpxy) * 1.50, 2)
    elif nse_action == "Bull":
        return round(float(timpxy) * 1.00, 2)
    elif nse_action == "Bear":
        return round(float(timpxy) * 0.75, 2)
    elif nse_action == "Bearish":
        return round(float(timpxy) * 0.50, 2)
    else:
        # Default value when none of the conditions are met
        return 7

if __name__ == "__main__":
    # Example usage:
    timpxy_value = 10.0  # Replace with your actual value
    nse_action_value = "Bullish"  # Replace with your actual value
    trgtpxy_result = calculate_trgtpxy(timpxy_value, nse_action_value)
    print("trgtpxy Result:", trgtpxy_result)
