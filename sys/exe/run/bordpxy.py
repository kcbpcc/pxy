# bordpxy.py
from acvaluepxy import process_acvalue, get_current_acvalue
from clorpxy import SILVER, UNDERLINE, RED, GREEN, YELLOW, RESET, BRIGHT_YELLOW, BRIGHT_RED, BRIGHT_GREEN, BOLD, GREY
import subprocess

def printbord(total_nrml_m2m, total_cnc_m2m, optpxy, Day_Change, result, total_PnL_percentage, total_dPnL, total_PnL, total_dPnL_percentage,
             result_nrml, total_PnL_stocks_buy, total_PnL_options_buy, available_cash,
             nse_action, nse_power, all_Stocks_count, red_Stocks_count, green_Stocks_count, all_Stocks_capital_lacks, all_Stocks_worth_lacks, zero_qty_count, green_Stocks_profit_loss, green_Stocks_capital_rercentage, mktpxy, nrmlall_Stocks_count, nrmlall_Stocks_capital, nrmlall_Stocks_worth, nrmlall_Stocks_profit_loss, nsma):
    output_lines = []
    color_code = ""
    if mktpxy in ["Buy", "Bull"]:
        color_code = BRIGHT_GREEN + UNDERLINE
    elif mktpxy in ["Sell", "Bear"]:
        color_code = BRIGHT_RED + UNDERLINE
    text = "PXY® PreciseXceleratedYield Pvt Ltd™"
    print(color_code + text.center(42) + RESET)
    acvalue = ((all_Stocks_capital_lacks) + (available_cash/100000))  
    process_acvalue(acvalue)
    acvalue_to_print, ydaypnl_to_print = get_current_acvalue()           
    
    capital = 18.50
    hide = 5.00
    profit = (acvalue_to_print - capital)
    column_width = 30
    

    left_aligned_format = "{:<" + str(column_width) + "}"
    right_aligned_format = "{:>" + str(column_width) + "}"
    
    output_lines.append(left_aligned_format.format(f"A/C Capital:{BRIGHT_YELLOW}{round(capital, 2)}{RESET}") +
                        right_aligned_format.format(f"A/C Value:{BRIGHT_YELLOW}{round((acvalue_to_print + hide), 2)}{RESET}"))
    output_lines.append(left_aligned_format.format(f"A/C Profit:{BRIGHT_GREEN if (acvalue_to_print - capital) > 0 else BRIGHT_RED}{round((acvalue_to_print - capital ), 2)}{RESET}") +
                        right_aligned_format.format(f"A/C Loss:{BRIGHT_GREEN if total_PnL >= 0 else BRIGHT_RED}{round((total_PnL/100000), 2)}{RESET}"))
    output_lines.append(left_aligned_format.format(f"Flush:{BRIGHT_GREEN if green_Stocks_profit_loss > 0 else BRIGHT_RED}{round(green_Stocks_profit_loss)}{RESET}") +
                        right_aligned_format.format(f"Flush%:{BRIGHT_GREEN if green_Stocks_capital_rercentage > 1.4 else BRIGHT_RED}{green_Stocks_capital_rercentage}{RESET}"))                                  
    output_lines.append(
        left_aligned_format.format(
            f"{BRIGHT_YELLOW}{'Green'.zfill(3)}{RESET}:{str(green_Stocks_count).zfill(3)}"
            f"{BRIGHT_GREEN if mktpxy in ['Bull', 'Buy'] else BRIGHT_RED}"
            f"          {BOLD}{UNDERLINE}PXY{RESET}{BRIGHT_GREEN if mktpxy in ['Bull', 'Buy'] else BRIGHT_RED}"
        ) +
        right_aligned_format.format(
            f"{BRIGHT_GREEN if optpxy in ['Bull', 'Buy'] else BRIGHT_RED}"
            f"{BOLD}{UNDERLINE}®{RESET}            {BRIGHT_YELLOW}{'Red'.zfill(3)}{RESET}:{str(red_Stocks_count).zfill(3)}"
        )
    )
    output_lines.append(left_aligned_format.format(f"Capital:{BRIGHT_YELLOW}{round(all_Stocks_capital_lacks, 2)}{RESET}") + 
                      right_aligned_format.format(f"Value:{BRIGHT_YELLOW}{round(all_Stocks_worth_lacks, 2)}{RESET}"))
    output_lines.append(left_aligned_format.format(f"Delta:{BRIGHT_GREEN if ydaypnl_to_print >= 0 else BRIGHT_RED}{int(ydaypnl_to_print*100000)}{RESET}") +
                        right_aligned_format.format(f"P-P&L:{BRIGHT_GREEN if total_cnc_m2m > 0 else BRIGHT_RED}{str(int(total_cnc_m2m)).zfill(5)}{RESET}"))
    output_lines.append(left_aligned_format.format(f"Funds:{BRIGHT_GREEN if available_cash > 12000 else BRIGHT_YELLOW}{available_cash:.0f}{RESET}") +
                        right_aligned_format.format(f"Day-P&L:{BRIGHT_GREEN if total_dPnL >= 0 else BRIGHT_RED}{round(total_dPnL, 2)}{RESET}"))
    output_lines.append(left_aligned_format.format(f"Extras:{BRIGHT_GREEN if total_nrml_m2m >= 0 else BRIGHT_RED}{str(int(total_nrml_m2m)).zfill(5)}{RESET}") +
                      right_aligned_format.format(f"Booked:{BRIGHT_GREEN if result > 0 else BRIGHT_RED}{str(round(result)).zfill(5)}{RESET}"))

    full_output = '\n'.join(output_lines)
    print(full_output)
    subprocess.run(['python3', 'worldpxy.py']) 
    with open("bordpxy.csv", "w") as file:
        file.write(full_output)
    
