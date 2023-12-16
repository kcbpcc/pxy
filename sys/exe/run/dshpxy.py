import pandas as pd
from rich.console import Console
from rich.table import Table
from rich import box
from colorama import Fore, Style
import traceback

def convert_to_laks(value):
    return f'{value/100000:.4f}'

def format_value(value):
    if value == 'Profit & Loss':
        return '💵 Profit & Loss 💵'
    return f'{value:.0f}' if isinstance(value, (int, float)) else value

def colorize(row_index, value):
    if row_index == 3:  # 4th row
        try:
            numeric_value = float(value)
            if numeric_value > 0:
                return f'{Fore.GREEN}{Style(bright=True)}{format_value(value)}{Style.RESET_ALL}'
            elif numeric_value < 0:
                return f'{Fore.RED}{Style(bright=True)}{format_value(value)}{Style.RESET_ALL}'
            else:
                return f'{Style(bright=True)}{format_value(value)}{Style.RESET_ALL}'
        except ValueError:
            return format_value(value)
    else:
        return format_value(value)

def get_holdingsinfo(csv_file_path):
    try:
        # ... (rest of the code remains unchanged)

        console = Console(width=42)
        table = Table(show_header=True, header_style="bold magenta", box=box.SIMPLE)

        table.add_column("⏰Laks", style="cyan", justify="right", width=10)
        table.add_column(" 🟢🔴🟢", style="green", justify="right", width=10)
        table.add_column(" 🟩🟩🟩", style="green", justify="right", width=10)
        table.add_column(" 🟥🟥🟥", style="red", justify="right", width=10)

        # Loop through rows and add data to the table
        for row_index in range(4):
            table.add_row(
                colorize(row_index, "📈Count" if total_Stocks_count else ""),  # Ensure there's always a value
                colorize(row_index, str(total_Stocks_count)),
                colorize(row_index, str(green_Stocks_count)),
                colorize(row_index, str(red_Stocks_count)),
            )

        # ... (rest of the code remains unchanged)

        console.print(table)

        print("  Number of Stocks Sold 💸💸💸: {}".format(zero_qty_count))
        print(" " * 42)
    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()
        return None

# Call the function with the path to your CSV file
get_holdingsinfo('fileHPdf.csv')




