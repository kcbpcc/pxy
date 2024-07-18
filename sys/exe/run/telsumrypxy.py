from utcpxy import peak_time

# Function to check if it's peak end
def is_peak_end():
    peak = peak_time()
    return peak == 'PEAKEND'

# Check if it's peak end
if is_peak_end():
    # Generate current date and time
    current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Generate a summary for Telegram
    summary = (
        f"Date and Time: {current_datetime}\n"
        f"BANKNIFTY: {bmktpredict} {arrow_map.get(bmktpxy, '')}\n"
        f"NIFTYNDEX: {mktpredict} {arrow_map.get(mktpxy, '')}\n"
        f"Margin: {available_cash}\n"
        f"Delta: {ydaypnl_to_print * 100000}\n"
        f"Real-P&L: {round((acvalue_to_print - capital + hide), 2)}\n"
        f"Run-P&L: {round(((all_Stocks_capital_lacks - all_Stocks_worth_lacks) * -1), 2)}\n"
        f"Capital: {capital}\n"
        f"Value: {acvalue_to_print}\n"
        f"Flush#: {green_Stocks_count}\n"
        f"Flush%: {green_Stocks_capital_percentage}%\n"
        f"CE/PE%: {optworth:.2f}%\n"
        f"Flush: {green_Stocks_profit_loss}\n"
        f"Positions: {total_cnc_m2m_postions}\n"
        f"Holdings: {all_Stocks_worth_dpnl}\n"
        f"Options: {total_opt_m2m}\n"
        f"BOOKED: {booked}\n"
        f"CLOSED: {extras}\n"
        f"PROFIT: {booked + extras}\n"
    )
    
    # Send summary to Telegram
    import requests
    
    TELEGRAM_BOT_TOKEN = "7163187536:AAG4UaLEj-iUlHENQmnNVE6080E1fZ_Wxtc"
    TELEGRAM_CHAT_ID = "-4143295985"
    message = summary
    
    telegram_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    params = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    
    response = requests.get(telegram_url, params=params)
    
    # Check if the message was sent successfully
    if response.status_code == 200:
        print("Message sent successfully!")
        # Update the log file with today's date
        update_log_file(log_file)
    else:
        None
else:
    None
