# Import market check and action functions
from mktpxy import get_market_check_handler
bbnkonemincandlesequance, bmktpxy = get_market_check_handler('^NSEBANK')
nonemincandlesequance, mktpxy = get_market_check_handler('^NSEI')

from bftpxy import get_bnk_action
ha_bnk_action, bnk_power, bDay_Change, bOpen_Change = get_bnk_action()

from nftpxy import ha_nse_action, nse_power, Day_Change, Open_Change

# Additional logic to place buy orders for BANKNIFTY and NIFTY based on 'PL%' < -50
def place_buy_orders_based_on_pl(df, broker):
    try:
        for index, row in df.iterrows():
            if row['PL%'] < -50:
                qty = 0
                can_average = False

                if row['key'].startswith('BANKNIFTY'):
                    current_qty = row['qty']
                    if current_qty < 30 and current_qty + 15 <= 45:  
                        qty = 15
                        if 'PE' in row['key']:
                            can_average = bnk_power > 0.9 and bmktpxy == 'Sell'
                        elif 'CE' in row['key']:
                            can_average = bnk_power < 0.1 and bmktpxy == 'Buy'
                elif row['key'].startswith('NIFTY'):
                    current_qty = row['qty']
                    if current_qty < 50 and current_qty + 25 <= 75: 
                        qty = 25
                        if 'PE' in row['key']:
                            can_average = bnk_power > 0.9 and mktpxy == 'Sell'
                        elif 'CE' in row['key']:
                            can_average = bnk_power < 0.1 and mktpxy == 'Buy'
                else:
                    continue

                if can_average:
                    print(f"Placing BUY order for {row['key']} with quantity {qty}")
                    order_id = place_order(row['key'], qty, 'BUY', 'MARKET', 'NRML', broker)

                    if order_id:
                        message = (
                            f"🚀🚀🚀 🤑🤑🤑 BUY order placed {row['key']} successfully.\n"
                            f"PL%: {round(row['PL%'], 2)}%\n"
                            f"Quantity: {qty}\n"
                        )
                        print(message)
                        send_telegram_message(message)
                else:
                    print(f"Skipping BUY order for {row['key']} due to bnk_power, market conditions, or qty limit.")
    except Exception as e:
        print(f"Error placing BUY order: {e}")

# Call the function to place buy orders
place_buy_orders_based_on_pl(final_df, broker)
