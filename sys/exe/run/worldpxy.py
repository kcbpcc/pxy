import requests
from bs4 import BeautifulSoup
from textblob import TextBlob
from rich import print
from rich.console import Console
from rich.style import Style

# Define the URL of MoneyControl's stock markets page for India
india_url = "https://www.moneycontrol.com/stocksmarketsindia/"

# Send an HTTP GET request to MoneyControl's stock markets page for India
india_response = requests.get(india_url)

# Define the URL of Yahoo Finance's global news page
global_url = "https://finance.yahoo.com/"

# Send an HTTP GET request to the global news page
global_response = requests.get(global_url)

# Initialize sentiment scores
india_sentiment = 0
global_sentiment = 0

if india_response.status_code == 200:
    # Parse the HTML content of MoneyControl's stock markets page for India using BeautifulSoup
    india_soup = BeautifulSoup(india_response.text, "html.parser")

    # Find the elements that contain Indian news headlines
    india_news_elements = india_soup.find_all("a", class_="ga-link")

    # Extract and display the Indian headlines (limit to 10)
    console = Console()
    console.print("Indian Financial News Headlines (MoneyControl):")
    for i, element in enumerate(india_news_elements[:10]):  # Limit to 10 headlines
        headline = element.text.strip()  # Remove leading/trailing whitespace
        console.print(f"Indian Headline {i + 1}: {headline}")

        # Analyze sentiment for Indian headlines
        sentiment_score = TextBlob(headline).sentiment.polarity
        india_sentiment += sentiment_score

    # Determine overall sentiment for India
    india_sentiment_summary = "Bullish" if india_sentiment > 0 else "Bearish" if india_sentiment < 0 else "Neutral"

    # Define styles for different sentiments
    bullish_style = Style(color="green")
    bearish_style = Style(color="red")
    neutral_style = Style(color="default")

    # Display overall sentiment with color
    console.print(f"[{bullish_style}]Overall Indian Stock Market Sentiment (MoneyControl): {india_sentiment_summary}[/{bullish_style}]")

    if global_response.status_code == 200:
        # Parse the HTML content of the global news page using BeautifulSoup
        global_soup = BeautifulSoup(global_response.text, "html.parser")

        # Find the elements that contain global news headlines
        global_news_elements = global_soup.find_all("h3")

        # Extract and display the global headlines (limit to 7)
        console.print("Global Financial News Headlines (Yahoo Finance):")
        for i, element in enumerate(global_news_elements[:7]):
            headline = element.text.strip()  # Remove leading/trailing whitespace
            console.print(f"Global Headline {i + 1}: {headline}")

            # Analyze sentiment for global headlines
            sentiment_score = TextBlob(headline).sentiment.polarity
            global_sentiment += sentiment_score

        # Determine overall sentiment for the world
        global_sentiment_summary = "Bullish" if global_sentiment > 0 else "Bearish" if global_sentiment < 0 else "Neutral"

        # Display overall sentiment for global news with color
        console.print(f"[{bullish_style}]Overall Global Stock Market Sentiment (Yahoo Finance): {global_sentiment_summary}[/{bullish_style}]")

    else:
        print("Failed to retrieve global financial news data from Yahoo Finance.")

else:
    print("Failed to retrieve Indian financial news data from MoneyControl.")
