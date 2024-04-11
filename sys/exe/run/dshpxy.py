import pandas as pd
from prettytable import PrettyTable

def convert_to_laks(value):
    return f'{value/100000:.4f}'

def format_value(value):
    if value == 'Profit & Loss':
        return 'Profit & Loss'
    return f'{value:.0f}' if isinstance(value, (int, float)) else value
from cmbddfpxy import process_data
combined_df = process_data()
def get_holdingsinfo(combined_df):
    try:
        if "m2m" not in combined_df.columns:
            combined_df['m2m'] = 0

        selected_holdings_df = combined_df[(combined_df['qty'] != 0) & (combined_df['product'] == 'CNC')]
        
        selected_holdings_df['cap'] = (selected_holdings_df['qty'] * selected_holdings_df['average_price']).astype(int)
        selected_holdings_df['unrealized'] = ((selected_holdings_df['ltp'] - selected_holdings_df['average_price']) * selected_holdings_df['qty']).round(2)
        selected_holdings_df['perc'] = ((selected_holdings_df['unrealized'] / selected_holdings_df['cap']) * 100)

        green_Stocks_df = selected_holdings_df[(selected_holdings_df['perc'] > 0)]
        green_Stocks_count = len(green_Stocks_df)
        green_Stocks_capital = green_Stocks_df['cap'].sum()
        green_Stocks_worth = green_Stocks_df['ltp'].dot(green_Stocks_df['qty']).round(4)
        green_Stocks_profit_loss = (green_Stocks_worth - green_Stocks_capital).round(4)
        green_Stocks_capital_percentage = round(((green_Stocks_worth - green_Stocks_capital) / green_Stocks_capital) * 100, 2) if green_Stocks_capital != 0 else 0

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

        day_change = all_Stocks_worth - selected_holdings_df['close_price'].dot(selected_holdings_df['qty']).round(4)
        day_change_percentage = ((day_change / selected_holdings_df['close_price'].dot(selected_holdings_df['qty']).round(4)) * 100) if selected_holdings_df['close_price'].dot(selected_holdings_df['qty']).round(4) != 0 else 0
        
        zero_qty_count = combined_df[combined_df['qty'] == 0].shape[0]
        all_Stocks_capital_lacks = all_Stocks_capital/100000
        all_Stocks_worth_lacks = all_Stocks_worth/100000

        selected_positions_df = combined_df[(combined_df['qty'] != 0) & (combined_df['product'] != 'CNC')]
        
        nrml_nfom2m_df = selected_positions_df.copy()
        nrml_nfom2m_df['m2m'] = pd.to_numeric(nrml_nfom2m_df['m2m'], errors='coerce')
        nrml_nfom2m_df['m2m'].fillna(0, inplace=True)
        total_nrml_m2m = nrml_nfom2m_df['m2m'].sum()

        nrmlall_Stocks_df = selected_positions_df[selected_positions_df['product'].isin(['NRML'])]
        nrmlall_Stocks_count = len(nrmlall_Stocks_df)
        nrmlall_Stocks_capital = nrmlall_Stocks_df['cap'].sum()
        nrmlall_Stocks_worth = (nrmlall_Stocks_df['ltp'] * nrmlall_Stocks_df['qty']).round(4).sum()
        nrmlall_Stocks_profit_loss = (nrmlall_Stocks_worth - nrmlall_Stocks_capital).round(4)

        return total_nrml_m2m, all_Stocks_count, red_Stocks_count, green_Stocks_count, all_Stocks_capital_lacks, all_Stocks_worth_lacks, zero_qty_count, green_Stocks_profit_loss, green_Stocks_capital_percentage

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Call the function with the combined_df
# get_holdingsinfo(combined_df)

# Assuming you have your DataFrame combined_df ready
result = get_holdingsinfo(combined_df)
if result is not None:
    nrmlall_Stocks_worth, total_nrml_m2m, all_Stocks_count, red_Stocks_count, green_Stocks_count, all_Stocks_capital_lacks, all_Stocks_worth_lacks, zero_qty_count, green_Stocks_profit_loss, green_Stocks_capital_percentage = result
    print(f"Total NRML M2M: {total_nrml_m2m}")
    print(f"All Stocks Count: {all_Stocks_count}")
    print(f"Red Stocks Count: {red_Stocks_count}")
    print(f"Green Stocks Count: {green_Stocks_count}")
    print(f"All Stocks Capital (in lakhs): {all_Stocks_capital_lacks}")
    print(f"All Stocks Worth (in lakhs): {all_Stocks_worth_lacks}")
    print(f"Zero Quantity Count: {zero_qty_count}")
    print(f"Green Stocks Profit/Loss: {green_Stocks_profit_loss}")
    print(f"Green Stocks Capital Percentage: {green_Stocks_capital_percentage}%")
