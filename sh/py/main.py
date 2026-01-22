from fyers_login import get_fyers

def main():
    fyers = get_fyers()
    profile = fyers.get_profile()

    print("\n🚀 FYERS READY")
    print(profile)

if __name__ == "__main__":
    main()
