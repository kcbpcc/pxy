import requests

# Your authentication credentials for the Upstock API
API_KEY = "d55a84b5-4234-4402-b2dd-400013d69fdb"
API_SECRET = "od4hoxf0rw"

# API endpoints
BASE_URL = "https://api.upstox.com/v2"
AUTH_ENDPOINT = "/auth"
HOLDINGS_ENDPOINT = "/holdings"



# Authenticate
auth_response = requests.post(BASE_URL + AUTH_ENDPOINT, json={"apiKey": API_KEY, "apiSecret": API_SECRET})
auth_data = auth_response.json()
access_token = auth_data.get("accessToken")

if access_token:
    # Get holdings
    headers = {"Authorization": f"Bearer {access_token}"}
    holdings_response = requests.get(BASE_URL + HOLDINGS_ENDPOINT, headers=headers)
    holdings_data = holdings_response.json()

    if holdings_response.status_code == 200:
        holdings = holdings_data.get("holdings")
        if holdings:
            for holding in holdings:
                print(holding)
        else:
            print("No holdings found.")
    else:
        print("Failed to retrieve holdings:", holdings_data.get("message"))
else:
    print("Authentication failed.")

