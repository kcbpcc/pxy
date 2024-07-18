import subprocess
from goouppxy import gsheet_acvalue
from googetpxy import get_ac_values
from mktpxy import get_market_check
from predictpxy import predict_market_sentiment
from bpredictpxy import predict_bnk_sentiment
from clorpxy import SILVER, UNDERLINE, RED, GREEN, YELLOW, RESET, BRIGHT_YELLOW, BRIGHT_RED, BRIGHT_GREEN, BOLD, GREY

def printbord(booked, total_cnc_m2m_postions, extras, optworth, all_Stocks_worth_dpnl, nsma, all_Stocks_yworth_lacks, total_opt_m2m, mktpxy, available_cash, ha_nse_action, nse_power, Day_Change, Open_Change, all_Stocks_count, red_Stocks_count, green_Stocks_count, all_Stocks_capital_lacks, all_Stocks_worth_lacks, zero_qty_count, green_Stocks_profit_loss, green_Stocks_capital_percentage):
    output_lines = []
    try:
        onemincandlesequance, bmktpxy = get_market_check('^NSEBANK')
        mktpredict = predict_market_sentiment()
        bmktpredict = predict_bnk_sentiment()

        acvalue = (all_Stocks_worth_lacks + optworth / 100000 + available_cash / 100000)
        gsheet_acvalue(acvalue)

        acvalue_to_print, ydaypnl_to_print = get_ac_values()
        if acvalue_to_print is None or ydaypnl_to_print is None:
            acvalue_to_print = 0
            ydaypnl_to_print = 0
    except Exception:
        acvalue_to_print = 0
        ydaypnl_to_print = 0

    capital = 17.82
    hide = 0
    profit = acvalue_to_print - capital

    arrow_map = {"Buy": "↗", "Sell": "↘", "Bull": "↑", "Bear": "↓"}
    column_width = 30
    left_aligned_format = "{:<" + str(column_width) + "}"
    right_aligned_format = "{:>" + str(column_width) + "}"

    output_lines.append(left_aligned_format.format(f"BANKNIFTY:{BRIGHT_GREEN if bmktpredict == 'RISE' else BRIGHT_RED if bmktpredict == 'FALL' else BRIGHT_YELLOW}{bmktpredict} {arrow_map.get(bmktpxy, '')}{RESET}") +
                       right_aligned_format.format(f"NIFTYNDEX:{BRIGHT_GREEN if mktpredict == 'RISE' else BRIGHT_RED if mktpredict == 'FALL' else BRIGHT_YELLOW}{mktpredict} {arrow_map.get(mktpxy, '')}{RESET}"))

    output_lines.append(left_aligned_format.format(f"Margin:{BRIGHT_GREEN if available_cash > 50000 else BRIGHT_YELLOW}{str(int(available_cash)).zfill(6)}{RESET}") +
                       right_aligned_format.format(f"Delta:{BRIGHT_GREEN if ydaypnl_to_print > 0 else BRIGHT_RED}{str(int(ydaypnl_to_print * 100000)).zfill(6)}{RESET}"))

    output_lines.append(left_aligned_format.format(f"Real-P&L:{BRIGHT_GREEN if (acvalue_to_print - capital + hide) > 0 else BRIGHT_RED}{round((acvalue_to_print - capital + hide), 2)}{RESET}") +
                       right_aligned_format.format(f"Run-P&L:{BRIGHT_GREEN if (all_Stocks_capital_lacks - all_Stocks_worth_lacks) * -1 >= 0 else BRIGHT_RED}{round(((all_Stocks_capital_lacks - all_Stocks_worth_lacks) * -1), 2)}{RESET}"))

    output_lines.append(left_aligned_format.format(f"{'Capital'.zfill(7)}:{BRIGHT_YELLOW}{str(round(capital, 2)).zfill(5)}{BRIGHT_GREEN if mktpxy in ['Bull', 'Buy'] else BRIGHT_RED}      {BOLD}{UNDERLINE}PXY{RESET}") +
                       right_aligned_format.format(f"{BRIGHT_GREEN if mktpxy in ['Bull'] else (BRIGHT_RED if mktpxy in ['Bear'] else GREY)}{BOLD}{UNDERLINE}®{RESET}{BRIGHT_YELLOW}{arrow_map.get(mktpxy, '')}{RESET}       {'Value'.zfill(5)}:{BRIGHT_YELLOW}{str(round(acvalue_to_print, 2)).zfill(5)}{RESET}"))

    output_lines.append(left_aligned_format.format(f"Flush#:{BRIGHT_GREEN if green_Stocks_capital_percentage > 0 else BRIGHT_RED}{str(round(green_Stocks_count)).zfill(3)}{RESET}") +
                       right_aligned_format.format(f"Flush%:{BRIGHT_GREEN if green_Stocks_capital_percentage > 0 else BRIGHT_RED}{str(round(green_Stocks_capital_percentage, 2)).zfill(4)}%{RESET}"))

    output_lines.append(left_aligned_format.format(f"CE/PE%:{BRIGHT_GREEN if 0.9 <= optworth <= 1.1 else BRIGHT_RED}{optworth:.2f}%{RESET}") +
                       right_aligned_format.format(f"Flush:{BRIGHT_GREEN if green_Stocks_profit_loss > 0 else BRIGHT_RED}{int(green_Stocks_profit_loss)}{RESET}"))

    output_lines.append(left_aligned_format.format(f"Positions:{BRIGHT_GREEN if total_cnc_m2m_postions > 0 else BRIGHT_RED}{int(round(total_cnc_m2m_postions, 0))}{RESET}") +
                       right_aligned_format.format(f"Holdings:{BRIGHT_GREEN if all_Stocks_worth_dpnl > 0 else BRIGHT_RED}{int(round(all_Stocks_worth_dpnl, 0))}{RESET}"))

    output_lines.append(left_aligned_format.format(f"Options:{BRIGHT_GREEN if total_opt_m2m > 0 else BRIGHT_RED}{str(int(total_opt_m2m)).zfill(5)}{RESET}") +
                       right_aligned_format.format(f"BOOKED:{GREEN if booked > 0 else RED}{str(int(booked)).zfill(5)}{RESET}"))

    output_lines.append(left_aligned_format.format(f"CLOSED:{BRIGHT_GREEN if extras >= 0 else BRIGHT_RED}{str(int(extras)).zfill(5)}{RESET}") +
                       right_aligned_format.format(f"PROFIT:{GREEN if (booked + extras) > 0 else RED}{str(round(booked + extras)).zfill(5)}{RESET}"))

    full_output = '\n'.join(output_lines)

    # Print the formatted output
    print(full_output)
    from datetime import datetime
    import requests
    from utcpxy import peak_time  # Assuming peak_time() function is defined in utcpxy module
    
    # Function to check if it's peak end
    def is_peak_end():
        peak = peak_time()
        return peak == 'PEAKEND'
    
    # Check if it's peak end
    if not is_peak_end(): #if is_peak_end(): 
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
        # Else block removed intentionally to ensure nothing is printed or done
