import pandas as pd
from rich.console import Console
from rich.table import Table
from rich import box
from colorama import Fore, Style  # Corrected import for Style
import traceback

def convert_to_laks(value):
    return f'{value/100000:.4f}'

def format_value(value):
    if value == 'Profit & Loss':
        return 'Profit & Loss'
    return f'{value:.0f}' if isinstance(value, (int, float)) else value

def colorize(value):
    if isinstance(value, (int, float)):
        if value < 0:
            return f'{Fore.RED}{Style(bright=True)}{format_value(value)}{Style.RESET_ALL}'
        elif value > 0:
            return f'{Fore.GREEN}{Style(bright=True)}{format_value(value)}{Style.RESET_ALL}'
        else:
            return f'{Style(bright=True)}{format_value(value)}{Style.RESET_ALL}'

def get_holdingsinfo(csv_file_path):
    try:
        holdings_df = pd.read_csv(csv_file_path)
        selected_holdings_df = holdings_df[holdings_df['qty'] != 0].copy()

        zero_qty_count = holdings_df[holdings_df['qty'] == 0].shape[0]


        selected_columns = ['tradingsymbol', 'qty', 'close_price', 'average_price', 'ltp']
        selected_holdings_df = selected_holdings_df[selected_columns].copy()

        selected_holdings_df['cap'] = (selected_holdings_df['qty'] * selected_holdings_df['average_price']).astype(int)
        selected_holdings_df['unrealized'] = ((selected_holdings_df['ltp'] - selected_holdings_df['average_price']) * selected_holdings_df['qty']).round(2)
        selected_holdings_df['perc'] = ((selected_holdings_df['unrealized'] / selected_holdings_df['cap']) * 100).where(selected_holdings_df['cap'] > 0)

        green_Stocks_df = selected_holdings_df[selected_holdings_df['perc'] > 0]
        red_Stocks_df = selected_holdings_df[selected_holdings_df['perc'] < 0]

        total_Stocks_count = len(selected_holdings_df)
        green_Stocks_count = len(green_Stocks_df)
        green_Stocks_capital = green_Stocks_df['cap'].sum()
        green_Stocks_worth = green_Stocks_df['ltp'].dot(green_Stocks_df['qty']).round(2)
        green_Stocks_profit_loss = (green_Stocks_worth - green_Stocks_capital).round(2)

        red_Stocks_count = len(red_Stocks_df)
        red_Stocks_capital = red_Stocks_df['cap'].sum()
        red_Stocks_worth = red_Stocks_df['ltp'].dot(red_Stocks_df['qty']).round(2)
        red_Stocks_profit_loss = (red_Stocks_worth - red_Stocks_capital).round(2)

        all_Stocks_capital = red_Stocks_df['cap'].sum() + green_Stocks_df['cap'].sum()
        all_Stocks_worth = green_Stocks_df['ltp'].dot(green_Stocks_df['qty']).round(2) + red_Stocks_df['ltp'].dot(red_Stocks_df['qty']).round(2)
        all_Stocks_profit_loss = (green_Stocks_worth - green_Stocks_capital).round(2) + (red_Stocks_worth - red_Stocks_capital).round(2)

        day_change = all_Stocks_worth - selected_holdings_df['close_price'].dot(selected_holdings_df['qty']).round(2)
        day_change_percentage = ((day_change / selected_holdings_df['close_price'].dot(selected_holdings_df['qty']).round(2)) * 100) if selected_holdings_df['close_price'].dot(selected_holdings_df['qty']).round(2) != 0 else 0

        console = Console(width=42)
        table = Table(show_header=True, header_style="bold magenta", box=box.SIMPLE)

        table.add_column("⏰Laks", style="cyan", justify="right", width=10)
        table.add_column(" 🟢🔴🟢", style="green", justify="right", width=10)
        table.add_column(" 🟩🟩🟩", style="green", justify="right", width=10)
        table.add_column(" 🟥🟥🟥", style="red", justify="right", width=10)

        table.add_row(
            "📈Count" if total_Stocks_count else "",  # Ensure there's always a value
            str(total_Stocks_count),
            str(green_Stocks_count),
            str(red_Stocks_count),
        )
        table.add_row(
            "💰Invst" if all_Stocks_capital else "",  # Ensure there's always a value
            convert_to_laks(all_Stocks_capital),
            convert_to_laks(green_Stocks_capital),
            convert_to_laks(red_Stocks_capital),
        )
        table.add_row(
            "🔄Worth" if all_Stocks_worth else "",  # Ensure there's always a value
            convert_to_laks(all_Stocks_worth),
            convert_to_laks(green_Stocks_worth),
            convert_to_laks(red_Stocks_worth),
        )

        table.add_row(
            "💵P&L💵" if all_Stocks_profit_loss else "",
            str(round(all_Stocks_profit_loss)),
            str(round(green_Stocks_profit_loss)),
            str(round(red_Stocks_profit_loss))
        )

        
        console.print(table)
        print(" " * 42)
        print("Number of Stocks Sold💸💸💸: {}".format(zero_qty_count))
    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()
        return None

# Call the function with the path to your CSV file
get_holdingsinfo('fileHPdf.csv')



