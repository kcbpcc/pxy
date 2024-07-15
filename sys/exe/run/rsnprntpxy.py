bnkmaxcount = 9
nftmaxcount = 1

from predictpxy import predict_market_sentiment
from bpredictpxy import predict_bnk_sentiment
from ordoptpxy import place_order
from telinoptpxy import send_telegram_message

async def process_orders(broker, available_cash, CE_position_exists, PE_position_exists, CE_symbol, PE_symbol, count_CE, count_PE):
    mktpxy = predict_market_sentiment()
    bmktpredict = predict_bnk_sentiment()

    try:
        if available_cash > 10000:
            await handle_orders(broker, CE_position_exists, PE_position_exists, CE_symbol, PE_symbol, count_CE, count_PE, mktpxy, bmktpredict)
        else:
            log_insufficient_funds(available_cash)
    except Exception as e:
        print(f"An error occurred: {str(e)}")

async def handle_orders(broker, CE_position_exists, PE_position_exists, CE_symbol, PE_symbol, count_CE, count_PE, mktpxy, bmktpredict):
    await handle_order(broker, CE_position_exists, CE_symbol, count_CE, mktpxy == 'Buy', 'BANKNIFTY', 'NIFTY', bnkmaxcount, nftmaxcount, bmktpredict)
    await handle_order(broker, PE_position_exists, PE_symbol, count_PE, mktpxy == 'Sell', 'BANKNIFTY', 'NIFTY', bnkmaxcount, nftmaxcount, bmktpredict)

async def handle_order(broker, position_exists, symbol, count, is_market_condition_met, banknifty_prefix, nifty_prefix, bnkmaxcount, nftmaxcount, bmktpredict):
    if not position_exists and is_market_condition_met:
        quantity = determine_quantity(symbol, count, banknifty_prefix, nifty_prefix, bnkmaxcount, nftmaxcount, bmktpredict)
        if quantity > 0:
            await execute_order(broker, symbol, quantity)
        else:
            print(f"Not placing as {symbol} Maxed")
    else:
        print_order_reason(symbol, position_exists, count, 'Hold')

def determine_quantity(symbol, count, banknifty_prefix, nifty_prefix, bnkmaxcount, nftmaxcount, bmktpredict):
    if symbol.startswith(banknifty_prefix) and count < bnkmaxcount:
        if symbol.endswith("PE") and bmktpredict == "FALL":
            return 30
        elif symbol.endswith("CE") and bmktpredict == "RISE":
            return 30
        else:
            return 15
    elif symbol.startswith(nifty_prefix) and count < nftmaxcount:
        return 50
    else:
        return 0

async def execute_order(broker, symbol, quantity):
    buy_order_placed, buy_order_id = await place_order(broker, symbol, 'BUY', 'NRML', quantity, 'MARKET')
    if buy_order_placed:
        await send_telegram_message(f"🛫🛫🛫 🌱🌱🌱 ENTRY order placed for {symbol} placed successfully.")
        print(f"{symbol} BUY order placed successfully.")
    else:
        print(f"Failed to place BUY order for {symbol}")

def print_order_reason(symbol, position_exists, count, action):
    reason = f"|{action}|{'✅' if position_exists else '🚫'}|"
    reason += "MaxOut" if count >= (bnkmaxcount if symbol.startswith('BANKNIFTY') else nftmaxcount) else ""
    if reason:
        print(f"{symbol}: {reason: >{39 - len(symbol)}}")

def log_insufficient_funds(available_cash):
    print(f"\033[91mNo sufficient funds available Cash💰: {int(round(available_cash/1000))}K\033[0m")


