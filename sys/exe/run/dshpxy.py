import pandas as pd
from prettytable import PrettyTable

def convert_to_laks(value):
    return f'{value/100000:.4f}'

def format_value(value):
    if value == 'Profit & Loss':
        return 'Profit & Loss'
    return f'{value:.0f}' if isinstance(value, (int, float)) else value

def get_holdingsinfo(combined_df):
    try:

        selected_holdings_df = combined_df.loc[combined_df['product'] == 'CNC'].copy()
        
        selected_holdings_df.loc[:, 'cap'] = (selected_holdings_df['qty'] * selected_holdings_df['average_price']).astype(int)
        selected_holdings_df.loc[:, 'unrealized'] = ((selected_holdings_df['ltp'] - selected_holdings_df['average_price']) * selected_holdings_df['qty']).round(2)
        selected_holdings_df.loc[:, 'perc'] = ((selected_holdings_df['unrealized'] / selected_holdings_df['cap']) * 100)

        green_Stocks_df = selected_holdings_df[(selected_holdings_df['pnl'] > 0) & (selected_holdings_df['source'] == 'holdings')].copy()
        green_Stocks_count = len(green_Stocks_df)
        green_Stocks_capital = green_Stocks_df['cap'].sum()
        green_Stocks_worth = (green_Stocks_df['ltp'] * green_Stocks_df['qty']).sum().round(4)
        green_Stocks_profit_loss = (green_Stocks_worth - green_Stocks_capital).round(4)
        green_Stocks_capital_percentage = round(((green_Stocks_worth - green_Stocks_capital) / green_Stocks_capital) * 100, 2) if green_Stocks_capital != 0 else 0

        red_Stocks_df = selected_holdings_df[selected_holdings_df['perc'] < 0].copy()
        red_Stocks_count = len(red_Stocks_df)
        red_Stocks_capital = red_Stocks_df['cap'].sum()
        red_Stocks_worth = (red_Stocks_df['ltp'] * red_Stocks_df['qty']).sum().round(4)
        red_Stocks_profit_loss = (red_Stocks_worth - red_Stocks_capital).round(4)

        all_Stocks_df =  selected_holdings_df[(selected_holdings_df['qty'] > 0) & (selected_holdings_df['product'] == 'CNC') & (selected_holdings_df['source'] == 'holdings')].copy()
        all_Stocks_count = len(selected_holdings_df)
        all_Stocks_capital = all_Stocks_df['cap'].sum()
        all_Stocks_yworth = (all_Stocks_df['close'] * all_Stocks_df['qty']).sum().round(4)
        all_Stocks_worth = (all_Stocks_df['ltp'] * all_Stocks_df['qty']).sum().round(4)
        all_Stocks_worth_dpnl = (all_Stocks_worth - all_Stocks_yworth)
        all_Stocks_profit_loss = (all_Stocks_worth - all_Stocks_capital).round(4)

        cnc_nfom2m_df = selected_holdings_df[(selected_holdings_df['key'].str.contains("NSE:|BSE:") & (selected_holdings_df['source'] == 'positions') & (selected_holdings_df['qty'] > 0))].copy()
        cnc_nfom2m_df['m2m'] = pd.to_numeric(cnc_nfom2m_df['m2m'], errors='coerce')
        cnc_nfom2m_df['m2m'].fillna(0, inplace=True)
        total_cnc_m2m = cnc_nfom2m_df['m2m'].sum()

        day_change = all_Stocks_worth - (selected_holdings_df['close_price'] * selected_holdings_df['qty']).sum().round(4)
        day_change_percentage = ((day_change / (selected_holdings_df['close_price'] * selected_holdings_df['qty']).sum().round(4)) * 100) if (selected_holdings_df['close_price'] * selected_holdings_df['qty']).sum().round(4) != 0 else 0
        
        zero_qty_count = combined_df[combined_df['qty'] == 0].shape[0]
        all_Stocks_capital_lacks = all_Stocks_capital / 100000
        all_Stocks_worth_lacks = all_Stocks_worth / 100000
        all_Stocks_yworth_lacks = all_Stocks_yworth / 100000
        green_Stocks_capital_lacks = green_Stocks_capital / 100000
        red_Stocks_capital_lacks = red_Stocks_capital / 100000

        selected_opts_df = combined_df[(combined_df['qty'] != 0) & combined_df['key'].str.contains('NFO:', case=False)].copy()
        total_opts_invested_lacks = selected_opts_df['Invested'].sum() / 100000

        optworth = combined_df.loc[combined_df['key'].str.contains('NFO:'), 'value'].sum()
        nfo_df = combined_df.loc[(combined_df['key'].str.contains('NFO:'))]

        if not nfo_df.empty:
            extras = nfo_df.loc[nfo_df['qty'] == 0, 'unrealised'].sum()
            open = nfo_df.loc[nfo_df['qty'] > 0, 'unrealised'].sum()
        else:
            extras = 0  # or any default value you prefer when there are no rows matching the condition
            open = 0  # Ensure this is also initialized in the else block

        return open, extras, optworth, all_Stocks_worth_dpnl, all_Stocks_yworth_lacks, total_cnc_m2m, all_Stocks_count, red_Stocks_count, green_Stocks_count, all_Stocks_capital_lacks, all_Stocks_worth_lacks, zero_qty_count, green_Stocks_profit_loss, green_Stocks_capital_percentage

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Call the function with the combined_df
# get_holdingsinfo(combined_df)
# Call the function with the combined_df
# get_holdingsinfo(combined_df)
