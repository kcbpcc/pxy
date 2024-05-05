async def process_orders(broker, available_cash, CE_position_exists, PE_position_exists, CE_symbol, PE_symbol, count_CE, count_PE, mktpxy):
    if available_cash > 10000:
        if not CE_position_exists and mktpxy == 'Buy' and count_CE < 3:
            buy_order_placed_CE, buy_order_id_CE = await place_order(broker, CE_symbol, 'BUY', 'NRML', 15, 'MARKET')
            if buy_order_placed_CE:
                await send_telegram_message(f"🛫🛫🛫 👉👉👉 ENTRY order placed for {CE_symbol} placed successfully.")
                print(f"{CE_symbol} BUY order placed successfully.")
        else:
            reason = f"exists:{'Y' if CE_position_exists else 'N'} |" if CE_position_exists else ""
            reason += "not Buy'| " if mktpxy != 'Buy' else ""
            reason += "Have 3. " if count_CE >= 3 else ""
            print(f"{CE_symbol} : {reason}")

        if not PE_position_exists and mktpxy == 'Sell' and count_PE < 3:
            buy_order_placed_PE, buy_order_id_PE = await place_order(broker, PE_symbol, 'BUY', 'NRML', 15, 'MARKET')
            if buy_order_placed_PE:
                await send_telegram_message(f"🛫🛫🛫 👉👉👉 ENTRY order placed for {PE_symbol} placed successfully.")
                print(f"{PE_symbol} BUY order placed successfully.")
        else:
            reason = f"exists:{'Y' if PE_position_exists else 'N'} |" if PE_position_exists else ""
            reason += "not 'Sell'| " if mktpxy != 'Sell' else ""
            reason += "Have 3 " if count_PE >= 3 else ""
            print(f"{PE_symbol} : {reason}")

    else:
        print(f"\033[91mNo sufficient funds available Cash💰: {int(round(available_cash/1000))}K\033[0m")
