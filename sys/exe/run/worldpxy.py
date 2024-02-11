import requests
from bs4 import BeautifulSoup
from textblob import TextBlob
from rich.console import Console
from rich.style import Style

# Function to fetch sentiment for a given exchange
def fetch_sentiment(exchange):
    url = f"https://finance.yahoo.com/quote/%5E{exchange}/"
    response = requests.get(url)
    sentiment = None

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        sentiment_element = soup.find("span", {"data-reactid": "50"})
        if sentiment_element:
            sentiment = sentiment_element.text.strip()
    return sentiment

# Function to determine sentiment color
def sentiment_color(sentiment):
    if sentiment == "Bullish":
        return Style(color="green")
    elif sentiment == "Bearish":
        return Style(color="red")
    else:
        return Style(color="default")

# Dictionary of major stock exchanges with weights based on their significance
exchanges = {
    "DJI": {"name": "Dow Jones", "weight": 0.35},
    "IXIC": {"name": "Nasdaq", "weight": 0.30},
    "INX": {"name": "S&P 500", "weight": 0.35},
    "FTSE": {"name": "FTSE 100", "weight": 0.20},
    "GDAXI": {"name": "DAX", "weight": 0.15},
    "FCHI": {"name": "CAC 40", "weight": 0.15},
    "N225": {"name": "Nikkei 225", "weight": 0.20},
    "HSI": {"name": "Hang Seng Index", "weight": 0.20},
    "000001.SS": {"name": "Shanghai Composite", "weight": 0.20}
}

# Create a console object for rich text output
console = Console()

# Initialize variables for calculating overall sentiment
total_weighted_sentiment = 0
total_weight = 0

# Fetch sentiment for each exchange and print individual market sentiment
for exchange, details in exchanges.items():
    sentiment = fetch_sentiment(exchange)
    if sentiment:
        sentiment_style = sentiment_color(sentiment)
        console.print(f"{details['name']}: [{sentiment_style}]{sentiment}[/{sentiment_style}]")
        
        # Calculate weighted sentiment
        if sentiment == "Bullish":
            total_weighted_sentiment += details["weight"]
        elif sentiment == "Bearish":
            total_weighted_sentiment -= details["weight"]
        total_weight += details["weight"]

# Calculate overall sentiment if there's any sentiment available
if total_weight > 0:
    overall_sentiment = "Bullish" if total_weighted_sentiment > 0 else "Bearish" if total_weighted_sentiment < 0 else "Neutral"
    console.print(f"\nOverall Market Sentiment: {overall_sentiment}")
else:
    console.print("\nNo sentiment data available.")

