import sys
import traceback
import requests
from login_get_kite import get_kite, remove_token
from cnstpxy import dir_path
from toolkit.logger import Logger
import logging

# Initialize logging
logging = Logger(30, dir_path + "main.log")

try:
    # Bypass authentication method
    broker = get_kite(api="bypass", sec_dir=dir_path)
except Exception as e:
    remove_token(dir_path)
    print(traceback.format_exc())
    logging.error(f"{str(e)} unable to get holdings")
    sys.exit(1)

def ohlc(self, *instruments):
    """
    Retrieve OHLC and market depth for list of instruments.

    - `instruments` is a list of instruments, Instrument are in the format of `exchange:tradingsymbol`. For example NSE:INFY
    """
    ins = list(instruments)

    # If first element is a list then accept it as instruments list for legacy reason
    if len(instruments) > 0 and type(instruments[0]) == list:
        ins = instruments[0]

    return self._get("market.quote.ohlc", params={"i": ins})

def get_ltp(instrument_tokens, broker):
    headers = {
        "X-Kite-Version": "3",
        "Authorization": f"token {broker['api_key']}:{broker['access_token']}"
    }

    try:
        ltp_data = {}
        for instrument_token in instrument_tokens:
            url = f"https://api.kite.trade/quote/ltp?i={instrument_token}"
            response = requests.get(url, headers=headers)
            data = response.json()
            if response.status_code == 200 and "data" in data:
                ltp_data.update(data["data"])
            else:
                raise Exception(f"Failed to retrieve LTP for instrument token {instrument_token}")

            # Retrieve OHLC data
            ohlc_data = broker.ohlc(instrument_token)
            if ohlc_data:
                # Incorporate OHLC data into the ltp_data dictionary
                ltp_data[instrument_token]["ohlc"] = ohlc_data
            else:
                logging.warning(f"Failed to retrieve OHLC data for {instrument_token}")

        return ltp_data
    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()
        return None

if __name__ == "__main__":
    try:
        instrument_tokens = ['NSE:INFY', 'BSE:SENSEX', 'NSE:NIFTY+50']
        ltp_data = get_ltp(instrument_tokens, broker)
        if ltp_data:
            for symbol, info in ltp_data.items():
                ltp = info.get('last_price', 'N/A')
                ohlc = info.get('ohlc', {})
                print(f"{symbol}: Last Traded Price: {ltp}")
                print("OHLC Data:", ohlc)
        else:
            print("Failed to retrieve LTP data.")
    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()

