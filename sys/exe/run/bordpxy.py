import subprocess
from bukdpxy import sum_last_numerical_value_in_each_row
file_path = 'filePnL.csv'
booked = sum_last_numerical_value_in_each_row(file_path)
from acvaluepxy import process_acvalue, get_current_acvalue

from clorpxy import SILVER, UNDERLINE, RED, GREEN, YELLOW, RESET, BRIGHT_YELLOW, BRIGHT_RED, BRIGHT_GREEN, BOLD, GREY
def printbord(extras, optworth, all_Stocks_worth_dpnl, nsma, all_Stocks_yworth_lacks, total_cnc_m2m, mktpxy, available_cash, ha_nse_action, nse_power, Day_Change, Open_Change, all_Stocks_count, red_Stocks_count, green_Stocks_count, all_Stocks_capital_lacks, all_Stocks_worth_lacks, zero_qty_count, green_Stocks_profit_loss, green_Stocks_capital_percentage):
    output_lines = []
    acvalue = ((all_Stocks_worth_lacks) + (optworth / 100000) + (available_cash / 100000))  
    #print(f"all_Stocks_worth_lacks: {all_Stocks_worth_lacks}, optworth: {optworth}, available_cash: {available_cash}")
    #print("acvalue:", acvalue)
    process_acvalue(acvalue)
    acvalue_to_print, ydaypnl_to_print = get_current_acvalue()           
    capital = 18.50
    hide = 5.00
    profit = (acvalue_to_print - capital)
    column_width = 30
    left_aligned_format = "{:<" + str(column_width) + "}"
    right_aligned_format = "{:>" + str(column_width) + "}"

    output_lines.append(left_aligned_format.format(f"Profit:{BRIGHT_YELLOW}{round((acvalue_to_print - 15.10), 2)}{RESET}") +
                        right_aligned_format.format(f"Loss:{BRIGHT_GREEN if (all_Stocks_capital_lacks - all_Stocks_worth_lacks)*-1 >= 0 else BRIGHT_RED}{round(((all_Stocks_capital_lacks - all_Stocks_worth_lacks)*-1), 2)}{RESET}"))
    output_lines.append(left_aligned_format.format(f"Funds:{BRIGHT_GREEN if available_cash > 50000 else BRIGHT_YELLOW}{str(int(available_cash)).zfill(6)}{RESET}") +
                        right_aligned_format.format(f"Day-Delta:{BRIGHT_GREEN if ydaypnl_to_print > 0 else BRIGHT_RED}{int(ydaypnl_to_print * 100000)}{RESET}"))                                  
    output_lines.append(
        left_aligned_format.format(
            f"{'Capital'.zfill(7)}:{str(round(18.51, 2)).zfill(5)}"
            f"{BRIGHT_GREEN if mktpxy in ['Bull', 'Buy'] else BRIGHT_RED}"
            f"      {BOLD}{UNDERLINE}PXY{RESET}"
            f"{BRIGHT_GREEN if mktpxy in ['Bull'] else (BRIGHT_RED if mktpxy in ['Bear'] else GREY)}"
        ) +
        right_aligned_format.format(
            f"{BRIGHT_GREEN if mktpxy in ['Buy'] else (BRIGHT_RED if mktpxy in ['Sell'] else GREY)}"
            f"{BOLD}{UNDERLINE}®{RESET}        "
            f"{'Value'.zfill(5)}:{str(round(acvalue_to_print, 2)).zfill(5)}"
        )
    )
    output_lines.append(left_aligned_format.format(f"Day-Delta:{BRIGHT_GREEN if ydaypnl_to_print > 0 else BRIGHT_RED}{round(ydaypnl_to_print)}{RESET}") +
                        right_aligned_format.format(f"Day-P&L:{BRIGHT_GREEN if all_Stocks_worth_dpnl > 0 else BRIGHT_RED}{int(round(all_Stocks_worth_dpnl, 0))}{RESET}"))
    #output_lines.append(left_aligned_format.format(f"Postions:{BRIGHT_GREEN if total_cnc_m2m >= 0 else BRIGHT_RED}{int(total_cnc_m2m)}{RESET}") +
    output_lines.append(left_aligned_format.format(f"Extras:{BRIGHT_GREEN if extras >= 0 else BRIGHT_RED}{int(extras)}{RESET}") +                    
                        right_aligned_format.format(f"BOOKED:{GREEN if booked > 0 else GREEN}{str(round(booked)).zfill(5)}{RESET}"))
    full_output = '\n'.join(output_lines)
    with open("bordpxy.csv", "w") as file:
        file.write(full_output)
    print(full_output)
