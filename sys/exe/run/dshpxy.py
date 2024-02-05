import pandas as pd
from prettytable import PrettyTable
from colorama import Fore, Style


def convert_to_laks(value):
    return f'{value/100000:.4f}'

def format_value(value):
    if value == 'Profit & Loss':
        return 'Profit & Loss'
    return f'{value:.0f}' if isinstance(value, (int, float)) else value

def colorize(value):
    if isinstance(value, (int, float)):
        if value < 0:
            return f'{Fore.RED}{Style.BRIGHT}{format_value(value)}{Style.RESET_ALL}'
        elif value > 0:
            return f'{Fore.GREEN}{Style.BRIGHT}{format_value(value)}{Style.RESET_ALL}'
        else:
            return f'{Style.BRIGHT}{format_value(value)}{Style.RESET_ALL}'

def get_holdingsinfo(csv_file_path):
    try:
        # Read data from the local CSV file and filter out rows where qty is not equal to zero
        holdings_df = pd.read_csv(csv_file_path)
        selected_holdings_df = holdings_df[holdings_df['qty'] != 0].copy()
    
        selected_columns = ['tradingsymbol', 'qty', 'close_price', 'average_price', 'ltp']
        selected_holdings_df = selected_holdings_df[selected_columns].copy()
    
        selected_holdings_df['cap'] = (selected_holdings_df['qty'] * selected_holdings_df['average_price']).astype(int)
        selected_holdings_df['unrealized'] = ((selected_holdings_df['ltp'] - selected_holdings_df['average_price']) * selected_holdings_df['qty']).round(2)
        selected_holdings_df['perc'] = ((selected_holdings_df['unrealized'] / selected_holdings_df['cap']) * 100).where(selected_holdings_df['cap'] > 0)

        green_Stocks_df = selected_holdings_df[selected_holdings_df['perc'] > 1.4]
        green_Stocks_count = len(green_Stocks_df)
        green_Stocks_capital = green_Stocks_df['cap'].sum()
        green_Stocks_worth = green_Stocks_df['ltp'].dot(green_Stocks_df['qty']).round(4)
        green_Stocks_profit_loss = (green_Stocks_worth - green_Stocks_capital).round(4)
        green_Stocks_capital_rercentage  = round(((green_Stocks_worth - green_Stocks_capital) / green_Stocks_capital) * 100, 2)

        red_Stocks_df = selected_holdings_df[selected_holdings_df['perc'] < 0]
        red_Stocks_count = len(red_Stocks_df)
        red_Stocks_capital = red_Stocks_df['cap'].sum()
        red_Stocks_worth = red_Stocks_df['ltp'].dot(red_Stocks_df['qty']).round(4)
        red_Stocks_profit_loss = (red_Stocks_worth - red_Stocks_capital).round(4)

        all_Stocks_df = selected_holdings_df
        all_Stocks_count = len(selected_holdings_df)
        all_Stocks_capital = selected_holdings_df['cap'].sum()
        all_Stocks_worth = selected_holdings_df['ltp'].dot(selected_holdings_df['qty']).round(4)
        all_Stocks_profit_loss = (all_Stocks_worth - all_Stocks_capital).round(4)

        day_change = all_Stocks_worth - selected_holdings_df['close_price'].dot(selected_holdings_df['qty']).round(4)
        day_change_percentage = ((day_change / selected_holdings_df['close_price'].dot(selected_holdings_df['qty']).round(4)) * 100) if selected_holdings_df['close_price'].dot(selected_holdings_df['qty']).round(4) != 0 else 0
        table = PrettyTable()
        table.field_names = ['📉 Board', 'Total', 'Green', 'Red']
        table.add_row(['Stocks📈', all_Stocks_count, green_Stocks_count, red_Stocks_count])
        table.add_row(['Invested', convert_to_laks(all_Stocks_capital), convert_to_laks(green_Stocks_capital), convert_to_laks(red_Stocks_capital)])
        table.add_row(['WorthNow', convert_to_laks(all_Stocks_worth), convert_to_laks(green_Stocks_worth), convert_to_laks(red_Stocks_worth)])
        if all_Stocks_profit_loss < 0:
            table.add_row(['💰₹💰P&L', f'{Style.BRIGHT}{Fore.RED}{format_value(all_Stocks_profit_loss)}{Style.RESET_ALL}', colorize(green_Stocks_profit_loss), colorize(red_Stocks_profit_loss)])
        else:
            table.add_row(['💰₹💰P&L', f'{format_value(all_Stocks_profit_loss)}', colorize(green_Stocks_profit_loss), colorize(red_Stocks_profit_loss)])
        table.align = 'r'
        #print(table)
        zero_qty_count = holdings_df[holdings_df['qty'] == 0].shape[0]
        #print("Number of Stocks Sold 💸💸💸: {}".format(zero_qty_count).rjust(38))
        all_Stocks_capital_lacks = all_Stocks_capital/100000
        all_Stocks_worth_lacks = all_Stocks_worth/100000
        return red_Stocks_count, green_Stocks_count, all_Stocks_capital_lacks, all_Stocks_worth_lacks, zero_qty_count, green_Stocks_profit_loss, green_Stocks_capital_rercentage
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


# Call the function with the path to your CSV file
get_holdingsinfo('fileHPdf.csv')

get_holdingsinfo('fileHPdf.csv')

