from kiteconnect import KiteConnect
import webbrowser

# Step 1: Initialize API Key and Secret
api_key = "avku59f296gcvrv0"  # Replace with your API key
api_secret = "gip1xrf9mx5qtrg1ngb42svv8xl9xebp"  # Replace with your API secret

# Step 2: Initialize Kite Connect
kite = KiteConnect(api_key=api_key)

# Step 3: Generate and open login URL
login_url = kite.login_url()
print(f"Login URL: {login_url}")
webbrowser.open(login_url)

# Step 4: After login, manually extract the request_token from the redirected URL
request_token = input("Enter the request token received from the redirected URL: ")

try:
    # Step 5: Generate session and set access token
    data = kite.generate_session(request_token, api_secret=api_secret)
    access_token = data["access_token"]
    kite.set_access_token(access_token)
    print("Access Token: ", access_token)

    # Step 6: Fetch user profile
    profile = kite.profile()
    print("User Profile: ", profile)

    # Step 7: Get market quotes
    quote = kite.quote("NSE:RELIANCE")
    print("Market Quote for NSE:RELIANCE: ", quote)

    # Step 8: Place an order
    try:
        order_id = kite.place_order(
            tradingsymbol="RELIANCE",
            exchange=kite.EXCHANGE_NSE,
            transaction_type=kite.TRANSACTION_TYPE_BUY,
            quantity=1,
            order_type=kite.ORDER_TYPE_MARKET,
            product=kite.PRODUCT_CNC
        )
        print("Order placed. ID is:", order_id)
    except Exception as e:
        print(f"Error placing order: {e}")

    # Step 9: Fetch order history
    orders = kite.orders()
    print("Order History: ", orders)

except Exception as e:
    print(f"Error during authentication or API call: {e}")
