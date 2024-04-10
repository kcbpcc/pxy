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

def get_holdingsinfo(combined_df):
    try:
        # Use combined_df directly instead of reading from CSV
        selected_holdings_df = combined_df[(combined_df['qty'] != 0)]    
        
        selected_columns = ['tradingsymbol','key', 'm2m', 'product', 'qty', 'close_price', 'average_price', 'ltp']
        selected_holdings_df = selected_holdings_df[selected_columns].copy()
        nrml_nfom2m_df = combined_df[combined_df['key'].str.contains("NFO:")].copy()
        nrml_nfom2m_df['m2m'] = pd.to_numeric(nrml_nfom2m_df['m2m'], errors='coerce')
        nrml_nfom2m_df['m2m'].fillna(0, inplace=True)
        total_nrml_m2m = nrml_nfom2m_df['m2m'].sum()
        
        cnc_nfom2m_df = combined_df[(combined_df['key'].str.contains("NSE:|BSE:") & (combined_df['source'] == 'positions') & (combined_df['qty'] > 0))].copy()
        cnc_nfom2m_df['m2m'] = pd.to_numeric(cnc_nfom2m_df['m2m'], errors='coerce')
        cnc_nfom2m_df['m2m'].fillna(0, inplace=True)
        total_cnc_m2m = cnc_nfom2m_df['m2m'].sum()

        bkd_cnc_nfom2m_df = combined_df[(combined_df['key'].str.contains("NSE:|BSE:")) & (combined_df['source'] == 'holdings') & (combined_df['qty'] == 0)].copy()
        bkd_cnc_nfom2m_df['m2m'] = pd.to_numeric(bkd_cnc_nfom2m_df['m2m'], errors='coerce')
        bkd_cnc_nfom2m_df['m2m'].fillna(0, inplace=True)
        bkd_total_cnc_m2m = bkd_cnc_nfom2m_df['m2m'].sum()
        
        selected_holdings_df['cap'] = (selected_holdings_df['qty'] * selected_holdings_df['average_price']).astype(int)
        selected_holdings_df['unrealized'] = ((selected_holdings_df['ltp'] - selected_holdings_df['average_price']) * selected_holdings_df['qty']).round(2)
        selected_holdings_df['perc'] = ((selected_holdings_df['unrealized'] / selected_holdings_df['cap']) * 100).where(selected_holdings_df['cap'] > 0)

        green_Stocks_df = selected_holdings_df[selected_holdings_df['perc'] > 0] & [selected_holdings_df['product'] == 'CNC']
        green_Stocks_count = len(green_Stocks_df)
        green_Stocks_capital = green_Stocks_df['cap'].sum()
        green_Stocks_worth = green_Stocks_df['ltp'].dot(green_Stocks_df['qty']).round(4)
        green_Stocks_profit_loss = (green_Stocks_worth - green_Stocks_capital).round(4)
        green_Stocks_capital_rercentage = round(((green_Stocks_worth - green_Stocks_capital) / green_Stocks_capital) * 100, 2) if green_Stocks_capital != 0 else 0

        red_Stocks_df = selected_holdings_df[selected_holdings_df['perc'] < 0]
        red_Stocks_count = len(red_Stocks_df)
        red_Stocks_capital = red_Stocks_df['cap'].sum()
        red_Stocks_worth = red_Stocks_df['ltp'].dot(red_Stocks_df['qty']).round(4)
        red_Stocks_profit_loss = (red_Stocks_worth - red_Stocks_capital).round(4)

        all_Stocks_df = selected_holdings_df[selected_holdings_df['product'] == 'CNC']
        all_Stocks_count = len(selected_holdings_df)
        all_Stocks_capital = selected_holdings_df['cap'].sum()
        all_Stocks_worth = selected_holdings_df['ltp'].dot(selected_holdings_df['qty']).round(4)
        all_Stocks_profit_loss = (all_Stocks_worth - all_Stocks_capital).round(4)

        nrmlall_Stocks_df = selected_holdings_df[selected_holdings_df['product'].isin(['NRML'])]
        nrmlall_Stocks_count = len(nrmlall_Stocks_df)
        nrmlall_Stocks_capital = nrmlall_Stocks_df['cap'].sum()
        nrmlall_Stocks_worth = (nrmlall_Stocks_df['ltp'] * nrmlall_Stocks_df['qty']).round(4).sum()
        nrmlall_Stocks_profit_loss = (nrmlall_Stocks_worth - nrmlall_Stocks_capital).round(4)
        
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
        zero_qty_count = combined_df[combined_df['qty'] == 0].shape[0]
        all_Stocks_capital_lacks = all_Stocks_capital/100000
        all_Stocks_worth_lacks = all_Stocks_worth/100000
        return bkd_total_cnc_m2m, total_nrml_m2m, total_cnc_m2m, all_Stocks_count, red_Stocks_count, green_Stocks_count, all_Stocks_capital_lacks, all_Stocks_worth_lacks, zero_qty_count, green_Stocks_profit_loss, green_Stocks_capital_rercentage, nrmlall_Stocks_count, nrmlall_Stocks_capital, nrmlall_Stocks_worth, nrmlall_Stocks_profit_loss
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Call the function with the combined_df
#get_holdingsinfo(combined_df)


