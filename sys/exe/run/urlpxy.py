import webbrowser

urls = {
    "prf": "https://console.zerodha.com/verified/ba914521",
    "set": "https://trendlyne.com/fundamentals/your-parameters/updated-desc-param/",
    "chr": "https://www.tradingview.com/chart/bmZV8D16/?symbol=NSE%3ANIFTY",
    "gpt": "https://chat.openai.com/c/e1857754-dbaf-4ada-a0c9-2d97ce22177d",
    "git": "https://github.com/PreciseXceleratedYieldPXY/PXY",
}

def open_url(key):
    if key in urls:
        webbrowser.open(urls[key])
    else:
        print("Invalid key. Please choose a valid key.")

# Example usage
for key in urls:
    user_input = input(f"Press '{key}' to open the corresponding link: ")
    open_url(user_input)
