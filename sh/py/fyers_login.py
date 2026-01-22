import os
import json
from fyers_apiv3 import fyersModel
from settings import APP_ID, SECRET_KEY, REDIRECT_URI, TOKEN_FILE


def save_token(data):
    with open(TOKEN_FILE, "w") as f:
        json.dump(data, f, indent=2)


def load_token():
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "r") as f:
            return json.load(f)
    return None


def get_fyers():
    print("🔐 FYERS LOGIN")

    token_data = load_token()

    # ---------- REUSE TOKEN ----------
    if token_data and "access_token" in token_data:
        fyers = fyersModel.FyersModel(
            client_id=APP_ID,
            token=token_data["access_token"],
            log_path=""
        )

        profile = fyers.get_profile()
        if profile.get("code") == 200:
            print("✅ Using saved token")
            print(f"👤 User: {profile['data']['name']}")
            return fyers
        else:
            print("⚠ Saved token invalid, re-login required")

    # ---------- FRESH LOGIN ----------
    session = fyersModel.SessionModel(
        client_id=APP_ID,
        secret_key=SECRET_KEY,
        redirect_uri=REDIRECT_URI,
        response_type="code",
        grant_type="authorization_code"
    )

    auth_url = session.generate_authcode()
    print("\nOpen this URL in browser:\n")
    print(auth_url)
    print("\nPaste auth code below:")

    auth_code = input("AUTH CODE ➜ ").strip()
    session.set_token(auth_code)

    token_response = session.generate_token()
    if "access_token" not in token_response:
        raise Exception(f"Token generation failed: {token_response}")

    save_token(token_response)

    fyers = fyersModel.FyersModel(
        client_id=APP_ID,
        token=token_response["access_token"],
        log_path=""
    )

    profile = fyers.get_profile()
    print("✅ Login successful")
    print(f"👤 User: {profile['data']['name']}")

    return fyers
