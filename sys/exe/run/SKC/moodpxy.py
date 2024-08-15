from smapxy import get_sma
from daypxy import get_day
def get_mood(ticker_symbol):
    """
    Determine the market mood based on SMA trend and day metrics.
    """
    # Get the SMA trend and day metrics
    sma_trend = calculate_sma50(ticker_symbol)
    dayd, dayo, dayp, daya = calculate_day_metrics(ticker_symbol)
    
    # Determine the mood
    if dayo > 0 and sma_trend == "Up":
        return "Rise"
    elif dayo < 0 and sma_trend == "Down":
        return "Fall"
    else:
        return "Side"

def main():
    ticker_symbol = '^NSEI'  # Replace with the actual ticker symbol
    mood = get_mood(ticker_symbol)
    print(f"Mood: {mood}")

if __name__ == "__main__":
    mood = get_mood('^NSEI')
    print(f"Mood: {mood}")
