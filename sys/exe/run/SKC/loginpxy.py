import sys
import traceback
import logging
import os
from configpxy import dir_path

# Add the parent directory (cd1) to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from login_get_kite import get_kite, remove_token

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
