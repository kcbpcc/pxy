# common_utils.py

import sys
import traceback
import logging
from toolkit.currency import round_to_paise
from ..login_get_kite import get_kite, remove_token
from ..cnstpxy import dir_path

def get_login():
    try:
        original_stdout = sys.stdout
        with open('output.txt', 'w') as file:
            sys.stdout = file
            try:
                broker = get_kite()
                return broker
            except Exception as e:
                remove_token(dir_path)
                print(traceback.format_exc())
                logging.error(f"{str(e)} unable to get holdings")
                sys.exit(1)
    finally:
        sys.stdout = original_stdout
