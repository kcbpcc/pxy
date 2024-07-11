import subprocess
from bukdpxy import sum_last_numerical_value_in_each_row
file_path = 'filePnL.csv'
booked = sum_last_numerical_value_in_each_row(file_path)
from goouppxy import gsheet_acvalue
from googetpxy import get_ac_values
from mktpxy import get_market_check
onemincandlesequance, bmktpxy = get_market_check('^NSEBANK')
from clorpxy import SILVER, UNDERLINE, RED, GREEN, YELLOW, RESET, BRIGHT_YELLOW, BRIGHT_RED, BRIGHT_GREEN, BOLD, GREY
def printbord(total_cnc_m2m_postions, extras, optworth, all_Stocks_worth_dpnl, nsma, all_Stocks_yworth_lacks, total_opt_m2m, mktpxy, available_cash, ha_nse_action, nse_power, Day_Change, Open_Change, all_Stocks_count, red_Stocks_count, green_Stocks_count, all_Stocks_capital_lacks, all_Stocks_worth_lacks, zero_qty_count, green_Stocks_profit_loss, green_Stocks_capital_percentage):
    output_lines = []
    acvalue = ((all_Stocks_worth_lacks) + (optworth / 100000) + (available_cash / 100000))  
    #print(f"all_Stocks_worth_lacks: {all_Stocks_worth_lacks}, optworth: {optworth}, available_cash: {available_cash}")
    #print("acvalue:", acvalue)
    gsheet_acvalue(acvalue)
    try:
        acvalue_to_print, ydaypnl_to_print = get_ac_values()
        if acvalue_to_print is None or ydaypnl_to_print is None:
            # Handle the case where either value is None
            acvalue_to_print = 0
            ydaypnl_to_print = 0
    except Exception:
        # Handle any exceptions that occur during the execution of get_ac_values()
        acvalue_to_print = 0
        ydaypnl_to_print = 0
    capital = 17.82
    hide = 0
    profit = (acvalue_to_print - capital)
    arrow_map = {"Buy": "↗", "Sell": "↘", "Bull": "↑", "Bear": "↓"}
    column_width = 30
    left_aligned_format = "{:<" + str(column_width) + "}"
    right_aligned_format = "{:>" + str(column_width) + "}"
    output_lines.append(left_aligned_format.format(f"Funds:{BRIGHT_GREEN if available_cash > 50000 else BRIGHT_YELLOW}{str(int(available_cash)).zfill(6)}{RESET}") +
                        right_aligned_format.format(f"Delta:{BRIGHT_GREEN if ydaypnl_to_print > 0 else BRIGHT_RED}{str(int(ydaypnl_to_print * 100000)).zfill(6)}{RESET}"))
    output_lines.append(left_aligned_format.format(f"Real-P&L:{BRIGHT_GREEN if ((acvalue_to_print - capital)  + hide) > 0 else BRIGHT_RED}{round(((acvalue_to_print - capital)  + hide) , 2)}{RESET}") +
                        right_aligned_format.format(f"Run-P&L:{BRIGHT_GREEN if (all_Stocks_capital_lacks - all_Stocks_worth_lacks)*-1 >= 0 else BRIGHT_RED}{round(((all_Stocks_capital_lacks - all_Stocks_worth_lacks)*-1), 2)}{RESET}"))
    output_lines.append(left_aligned_format.format(f"BIFTY:{BRIGHT_GREEN if bmktpxy == 'Bull' else BRIGHT_RED if bmktpxy == 'Bear' else BRIGHT_YELLOW}{bmktpxy}{RESET}") +
                        right_aligned_format.format(f"NIFTY:{BRIGHT_GREEN if mktpxy == 'Bull' else BRIGHT_RED if bmktpxy == 'Bear' else BRIGHT_YELLOW}{mktpxy}{RESET}"))    
    output_lines.append(
        left_aligned_format.format(
            f"{'Capital'.zfill(7)}:{BRIGHT_YELLOW}{str(round(capital, 2)).zfill(5)}"
            f"{BRIGHT_GREEN if mktpxy in ['Bull', 'Buy'] else BRIGHT_RED}"
            f"      {BOLD}{UNDERLINE}PXY{RESET}"
        ) +
        right_aligned_format.format(
            f"{BRIGHT_GREEN if mktpxy in ['Bull'] else (BRIGHT_RED if mktpxy in ['Bear'] else GREY)}"
            f"{BOLD}{UNDERLINE}®{RESET}{BRIGHT_YELLOW}{arrow_map.get(mktpxy, '')}{RESET}       "  # Insert arrow_map here
            f"{'Value'.zfill(5)}:{BRIGHT_YELLOW}{str(round(acvalue_to_print, 2)).zfill(5)}{RESET}"
        )
    )
    output_lines.append(
        left_aligned_format.format(
            f"Flush#:{BRIGHT_GREEN if green_Stocks_capital_percentage > 0 else BRIGHT_RED}{str(round(green_Stocks_count)).zfill(3)}{RESET}"
        ) + right_aligned_format.format(
            f"Flush%:{BRIGHT_GREEN if green_Stocks_capital_percentage > 0 else BRIGHT_RED}{str(green_Stocks_capital_percentage).zfill(4)%}{RESET}"
        )
    )
    output_lines.append(left_aligned_format.format(f"Flush:{BRIGHT_GREEN if green_Stocks_profit_loss > 0 else BRIGHT_RED}{round(green_Stocks_profit_loss)}{RESET}") +
                        right_aligned_format.format(f"Pp&l:{BRIGHT_GREEN if total_cnc_m2m_postions > 0 else BRIGHT_RED}{str(int(total_cnc_m2m_postions))}{RESET}"))
    output_lines.append(left_aligned_format.format(f"Op&l:{BRIGHT_GREEN if total_opt_m2m > 0 else BRIGHT_RED}{int(round(total_opt_m2m, 0))}{RESET}") +
                        right_aligned_format.format(f"Hp&l:{BRIGHT_GREEN if all_Stocks_worth_dpnl > 0 else BRIGHT_RED}{int(round(all_Stocks_worth_dpnl, 0))}{RESET}"))
    output_lines.append(left_aligned_format.format(f"CLOSED:{BRIGHT_GREEN if extras >= 0 else BRIGHT_RED}{str(int(extras)).zfill(5)}{RESET}") +
                        right_aligned_format.format(f"BOOKED:{GREEN if booked > 0 else RED}{str(round(booked)).zfill(5)}{RESET}"))
    full_output = '\n'.join(output_lines)
    with open("bordpxy.csv", "w") as file:
        file.write(full_output)
    print(full_output)
