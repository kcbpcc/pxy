bnkmaxcount = 24
nftmaxcount = 24

from predictpxy import predict_market_sentiment
mktpredict = predict_market_sentiment()

from bpredictpxy import predict_bnk_sentiment
bmktpredict = predict_bnk_sentiment()

async def process_orders(broker, available_cash, CE_position_exists, PE_position_exists, CE_symbol, PE_symbol, count_CE, count_PE, mktpxy):
    from ordoptpxy import place_order
    from telinoptpxy import send_telegram_message

    try:
        if available_cash > 10000:
            if CE_symbol is not None and CE_position_exists is not None:
                await handle_CE_orders(broker, CE_position_exists, CE_symbol, count_CE, mktpxy, place_order, send_telegram_message, bnkmaxcount, nftmaxcount, bmktpredict)
            else:
                pass

            if PE_symbol is not None and PE_position_exists is not None:
                await handle_PE_orders(broker, PE_position_exists, PE_symbol, count_PE, mktpxy, place_order, send_telegram_message, bnkmaxcount, nftmaxcount, bmktpredict)
            else:
                pass
        else:
            log_insufficient_funds(available_cash)
    except Exception as e:
        print(f"An error occurred: {str(e)}")

async def handle_CE_orders(broker, CE_position_exists, CE_symbol, count_CE, mktpxy, place_order, send_telegram_message, bnkmaxcount, nftmaxcount, bmktpredict):
    if not CE_position_exists and mktpxy == 'Buy':
        quantity = determine_quantity(CE_symbol, count_CE, 'BANKNIFTY', 'NIFTY', bnkmaxcount, nftmaxcount, bmktpredict)
        if quantity > 0:
            await execute_order(broker, CE_symbol, quantity, place_order, send_telegram_message)
            print_order_reason(CE_symbol, CE_position_exists, count_CE, 'Hold')
        else:
            print(f"Not placing as {CE_symbol} Maxed")
    else:
        print_order_reason(CE_symbol, CE_position_exists, count_CE, 'Hold')

async def handle_PE_orders(broker, PE_position_exists, PE_symbol, count_PE, mktpxy, place_order, send_telegram_message, bnkmaxcount, nftmaxcount, bmktpredict):
    if not PE_position_exists and mktpxy == 'Sell':
        quantity = determine_quantity(PE_symbol, count_PE, 'BANKNIFTY', 'NIFTY', bnkmaxcount, nftmaxcount, bmktpredict)
        if quantity > 0:
            await execute_order(broker, PE_symbol, quantity, place_order, send_telegram_message)
        else:
            print(f"Not placing as {PE_symbol} Maxed")
    else:
        print_order_reason(PE_symbol, PE_position_exists, count_PE, 'Hold')

def determine_quantity(symbol, count, banknifty_prefix, nifty_prefix, bnkmaxcount, nftmaxcount, bmktpredict):
    if symbol.startswith(banknifty_prefix) and count < bnkmaxcount:
        if symbol.endswith("PE") and bmktpredict == "FALL":
            return 15
        elif symbol.endswith("CE") and bmktpredict == "RISE":
            return 15
        else:
            return 15
    elif symbol.startswith(nifty_prefix) and count < nftmaxcount:
        return 25
    else:
        return 0

async def execute_order(broker, symbol, quantity, place_order, send_telegram_message):
    buy_order_placed, buy_order_id = await place_order(broker, symbol, 'BUY', 'NRML', quantity, 'MARKET')
    if buy_order_placed:
        await send_telegram_message(f"🏹 Entry placed for {symbol}")
        print(f"🏹 {symbol:>22} successful")
    else:
        print(f"Failed to place BUY order for {symbol}")

def print_order_reason(symbol, position_exists, count, action):
    reason = f"|{action}|{'🥚' if position_exists else '🧺'}|"
    reason += "MaxOut" if count >= (bnkmaxcount if symbol.startswith('BANKNIFTY') else nftmaxcount) else ""
    if reason:
        print(f"{symbol}: {reason: >{39 - len(symbol)}}")

def log_insufficient_funds(available_cash):
    print(f"\033[91mNo sufficient funds available Cash💰: {int(round(available_cash/1000))}K\033[0m")
