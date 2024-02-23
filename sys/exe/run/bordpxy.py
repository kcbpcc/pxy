# bordpxy.py
from acvaluepxy import process_acvalue, get_current_acvalue
from optpxy import get_optpxy
import subprocess
optpxy = get_optpxy()
def printbord(Day_Change, result, total_PnL_percentage, total_dPnL, total_PnL, total_dPnL_percentage,
             result_nrml, total_PnL_cnc_buy, total_PnL_nrml_buy, available_cash, auto_value,
             nse_action, nse_power,red_Stocks_count,green_Stocks_count,all_Stocks_capital_lacks,all_Stocks_worth_lacks, zero_qty_count, green_Stocks_profit_loss, green_Stocks_capital_rercentage, mktpxy):                
    RESET = "\033[0m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    RESET = "\033[0m"
    output_lines = []
    print("━" * 42)
    #print("\033[93m📉🔀Trades Overview & Market Dynamics 📈🔄\033[0m")
    #print("━" * 42)
    auto_value_status = "Yes" if "AUTO" in auto_value else "No" if "MANUAL" in auto_value else None
    acvalue = ((all_Stocks_capital_lacks) + (available_cash/100000))  
    process_acvalue(acvalue)
    acvalue_to_print, ydaypnl_to_print = get_current_acvalue()           
    capital = 20
    profit = (acvalue_to_print - capital)
    column_width = 30
    left_aligned_format = "{:<" + str(column_width) + "}"
    right_aligned_format = "{:>" + str(column_width) + "}"
               
    output_lines.append(left_aligned_format.format(f"A/C Capital:{BRIGHT_YELLOW}{round(capital, 2)}{RESET}") +
                        right_aligned_format.format(f"A/C Value:{BRIGHT_YELLOW}{round(acvalue_to_print + 3.58, 2)}{RESET}"))
    output_lines.append(left_aligned_format.format(f"Total Profit:{BRIGHT_GREEN if profit > 0 else BRIGHT_RED}{round((profit+3.58), 2)}{RESET}") +
                        right_aligned_format.format(f"Total Loss:{BRIGHT_GREEN if total_PnL >= 0 else BRIGHT_RED}{round((total_PnL/100000), 2)}{RESET}"))
    #output_lines.append(left_aligned_format.format(f"Flush:{BRIGHT_GREEN if green_Stocks_profit_loss > 0 else BRIGHT_RED}{round(green_Stocks_profit_loss)}{RESET}") +
                            #right_aligned_format.format(f"Flush%:{BRIGHT_GREEN if green_Stocks_capital_rercentage > 1.4 else BRIGHT_RED}{green_Stocks_capital_rercentage}{RESET}"))                                  
    output_lines.append(
        left_aligned_format.format(
            f"Losers:{BRIGHT_RED}{str(red_Stocks_count).zfill(3)}{RESET}"
            f"{BRIGHT_GREEN if mktpxy in ['Bull', 'Buy'] else BRIGHT_RED}"
            f"         {BOLD}{UNDERLINE}PXY{RESET}{BRIGHT_GREEN if mktpxy in ['Bull', 'Buy'] else BRIGHT_RED}"
        ) +
        right_aligned_format.format(
            f"{BRIGHT_GREEN if optpxy in ['Bull', 'Buy'] else BRIGHT_RED}"
            f"{BOLD}{UNDERLINE}®{RESET}        Gainers:{BRIGHT_GREEN}{str(green_Stocks_count).zfill(3)}{RESET}"
        )
    )    
    output_lines.append(left_aligned_format.format(f"Funds:{BRIGHT_GREEN if available_cash > 12000 else BRIGHT_YELLOW}{available_cash:.0f}{RESET}") +
                        right_aligned_format.format(f"Winners:{BRIGHT_YELLOW}{zero_qty_count}{RESET}"))
    #output_lines.append(left_aligned_format.format(f"A/C Delta:{BRIGHT_GREEN if ydaypnl_to_print > 0 else BRIGHT_RED}{int((ydaypnl_to_print + 3.8)* 100000)}{RESET}") +
    
    output_lines.append(left_aligned_format.format(f"Opt Drive:{BRIGHT_GREEN if auto_value_status == 'Yes' else BRIGHT_RED}{auto_value}{RESET}") +
                        right_aligned_format.format(f"My Day:{BRIGHT_GREEN if total_dPnL_percentage >= 0 else BRIGHT_RED}{round(total_dPnL_percentage, 2)}%{RESET}"))
    output_lines.append(left_aligned_format.format(f"Options:{BRIGHT_GREEN if total_PnL_nrml_buy >= 0 else BRIGHT_RED}{int(total_PnL_nrml_buy)}{RESET}") +
                        right_aligned_format.format(f"Stocks:{BRIGHT_GREEN if total_PnL_cnc_buy >= 0 else BRIGHT_RED}{int(total_PnL_cnc_buy)}{RESET}")) 
    output_lines.append(left_aligned_format.format(f"Booked(opt):{BRIGHT_GREEN if result_nrml >= 0 else BRIGHT_RED}{str(int(result_nrml)).zfill(5)}{RESET}") +
                        right_aligned_format.format(f"Booked(stks):{BRIGHT_GREEN if result > 0 else BRIGHT_RED}{str(round(result)).zfill(5)}{RESET}"))
    output_lines.append(left_aligned_format.format(f"A/C Delta:{BRIGHT_GREEN if ydaypnl_to_print > 0 else BRIGHT_RED}{int((0)* 100000)}{RESET}") +
                        right_aligned_format.format(f"{BRIGHT_YELLOW}Day Profit:{BRIGHT_GREEN if (result_nrml+result) > 0 else BRIGHT_RED}{int(round((result_nrml+result), 2))}{RESET}")) 
    #print("━" * 42)  # Print another line of 42 dashes           
    #output_lines.append(f"{BRIGHT_YELLOW}Market is {nse_action} ⚡💥 - Power⚡💥{nse_power}{RESET}💥⚡")
    # Join the lines to create the full output
    full_output = '\n'.join(output_lines)
    # Print to console
    print(full_output)

    # Write to file
    with open("bordpxy.csv", "w") as file:
        file.write(full_output)

    # Write to file
    with open("bordpxy.csv", "w") as file:
        file.write(full_output)
