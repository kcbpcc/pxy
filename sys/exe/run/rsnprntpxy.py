async def process_orders(broker, available_cash, CE_position_exists, PE_position_exists, CE_symbol, PE_symbol, count_CE, count_PE, mktpxy):
    if available_cash > 10000:
        if not CE_position_exists and mktpxy == 'Buy' and count_CE < 3:
            if CE_symbol.startswith('BANKNIFTY'):
                quantity = 15
            elif CE_symbol.startswith('NIFTY'):
                quantity = 25
            else:
                quantity = 0  # Default quantity

            buy_order_placed_CE, buy_order_id_CE = await place_order(broker, CE_symbol, 'BUY', 'NRML', quantity, 'MARKET')
            if buy_order_placed_CE:
                await send_telegram_message(f"🛫🛫🛫 👉👉👉 ENTRY order placed for {CE_symbol} placed successfully.")
                print(f"{CE_symbol} BUY order placed successfully.")
        else:
            reason = f"{'Y' if CE_position_exists else 'N'}|not Buy |" if not CE_position_exists else ""
            reason += "Have 3" if count_CE >= 3 else ""
            if reason:
                print(f"{CE_symbol}: {reason: >{40 - len(CE_symbol)}}")
                print("━" * 42)

        if not PE_position_exists and mktpxy == 'Sell' and count_PE < 3:
            if PE_symbol.startswith('BANKNIFTY'):
                quantity = 15
            elif PE_symbol.startswith('NIFTY'):
                quantity = 25
            else:
                quantity = 0  # Default quantity

            buy_order_placed_PE, buy_order_id_PE = await place_order(broker, PE_symbol, 'BUY', 'NRML', quantity, 'MARKET')
            if buy_order_placed_PE:
                await send_telegram_message(f"🛫🛫🛫 👉👉👉 ENTRY order placed for {PE_symbol} placed successfully.")
                print(f"{PE_symbol} BUY order placed successfully.")
        else:
            reason = f"{'Y' if PE_position_exists else 'N'}|not Sell|" if not PE_position_exists else ""
            reason += "Have 3" if count_PE >= 3 else ""
            if reason:
                print(f"{PE_symbol}: {reason: >{40 - len(PE_symbol)}}")
                print("━" * 42)
    else:
        print(f"\033[91mNo sufficient funds available Cash💰: {int(round(available_cash/1000))}K\033[0m")

