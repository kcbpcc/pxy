import importlib
import subprocess
import time
import warnings
import sys
import os
import curses
from rich.console import Console
from sleeppxy import progress_bar
from predictpxy import predict_market_sentiment
from mktpxy import get_market_check
from nftpxy import get_nse_action
from utcpxy import peak_time
from macdpxy import calculate_macd_signal
from smapxy import check_index_status

# Function to initialize the curses screen
def init_curses():
    stdscr = curses.initscr()
    curses.cbreak()
    stdscr.keypad(True)
    curses.noecho()
    return stdscr

# Function to cleanup the curses screen
def cleanup_curses(stdscr):
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()

# Function to print output at a specific line of the terminal
def print_at_line(stdscr, line, output):
    stdscr.addstr(line, 0, output)
    stdscr.refresh()

# Initialize curses screen
stdscr = init_curses()

# Start the loop
lines_printed = 0  # Track the number of lines printed
while True:
    # Get new output
    mktpredict = predict_market_sentiment()
    onemincandlesequance, mktpxy = get_market_check('^NSEI')
    ha_nse_action, nse_power, Day_Change, Open_Change  = get_nse_action()
    peak = peak_time()
    macd = calculate_macd_signal("^NSEI")
    nsma = check_index_status('^NSEI')

    # Print new output at the top
    print_at_line(stdscr, 0, f"    PXY® Predicted market sentiment : {mktpredict}")
    progress_bar(5, mktpxy)
    
    # Reprint previous output below the new output
    if lines_printed > 0:
        print_at_line(stdscr, 2, "Previous output 1")
        print_at_line(stdscr, 3, "Previous output 2")
        # Repeat for other lines as needed

    # Update the number of lines printed
    lines_printed = 2  # Adjust this value based on the number of previous lines

    # Sleep for a while
    time.sleep(1)

# Cleanup curses screen
cleanup_curses(stdscr)


