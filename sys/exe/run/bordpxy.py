## bordpxy.py

def printbord(Day_Change, result, total_PnL_percentage, total_dPnL, total_PnL, total_dPnL_percentage,
             total_PnL_percentage_mis_sell, total_PnL_cnc_buy, mktpxy, available_cash, Open_Change,
             nse_action, nse_power,red_Stocks_count,green_Stocks_count,all_Stocks_capital_lacks,all_Stocks_worth_lacks, zero_qty_count, green_Stocks_profit_loss, green_Stocks_capital_rercentage):                
    RESET = "\033[0m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"

    output_lines = []
    print("-" * 42)
    print("\033[93m📉🔀Trades Overview & Market Dynamics 📈🔄\033[0m")
    print("-" * 42)
    column_width = 30
    left_aligned_format = "{:<" + str(column_width) + "}"
    right_aligned_format = "{:>" + str(column_width) + "}"

    output_lines.append(left_aligned_format.format(f"TotalPnL:{BRIGHT_GREEN if total_PnL >= 0 else BRIGHT_RED}{round(total_PnL, 2)}{RESET}") +
                        right_aligned_format.format(f"DayPnL:{BRIGHT_GREEN if total_dPnL > 0 else BRIGHT_RED}{round(total_dPnL, 2)}{RESET}"))
    output_lines.append(left_aligned_format.format(f"TotalPnL%:{BRIGHT_GREEN if total_PnL_percentage >= 0 else BRIGHT_RED}{round(total_PnL_percentage, 2)}{RESET}") +
                        right_aligned_format.format(f"DayPnL%:{BRIGHT_GREEN if total_dPnL_percentage > 0 else BRIGHT_RED}{round(total_dPnL_percentage, 2)}{RESET}"))
    output_lines.append(left_aligned_format.format(f"Intraday:{BRIGHT_GREEN if total_PnL_percentage_mis_sell >= 0 else BRIGHT_RED}{total_PnL_percentage_mis_sell}{RESET}") +
                        right_aligned_format.format(f"Delivery:{BRIGHT_GREEN if total_PnL_cnc_buy >= 0 else BRIGHT_RED}{total_PnL_cnc_buy}{RESET}"))   
    output_lines.append(left_aligned_format.format(f"Capital:{BRIGHT_YELLOW}{round(all_Stocks_capital_lacks, 2)}{RESET}") +
                        right_aligned_format.format(f"Value:{BRIGHT_YELLOW }{round(all_Stocks_worth_lacks, 2)}{RESET}"))             
    output_lines.append(left_aligned_format.format(f"Losers:{BRIGHT_RED }{red_Stocks_count}{RESET}") +
                        right_aligned_format.format(f"Gainers:{BRIGHT_GREEN }{green_Stocks_count}{RESET}"))
    output_lines.append(left_aligned_format.format(f"Funds:{BRIGHT_GREEN if available_cash > 12000 else BRIGHT_YELLOW}{available_cash:.0f}{RESET}") +
                        right_aligned_format.format(f"Winners:{BRIGHT_YELLOW}{zero_qty_count}{RESET}"))
    output_lines.append(left_aligned_format.format(f"Open%:{BRIGHT_GREEN if Open_Change >= 0 else BRIGHT_RED}{round(Open_Change, 2)}{RESET}") +
                        right_aligned_format.format(f"MKTPXY:{BRIGHT_GREEN if 'Buy' in mktpxy or 'Bull' in mktpxy else BRIGHT_RED}{mktpxy}{RESET}"))
    output_lines.append(left_aligned_format.format(f"Change%:{BRIGHT_GREEN if Day_Change >= 0 else BRIGHT_RED}{round(Day_Change, 2)}{RESET}") +
                        right_aligned_format.format(f"Flush%:{BRIGHT_GREEN if green_Stocks_capital_rercentage > 1.4 else BRIGHT_RED}{green_Stocks_capital_rercentage}{RESET}"))                   
    output_lines.append(left_aligned_format.format(f"Power:{BRIGHT_GREEN if nse_power > 0.5 else BRIGHT_RED}{nse_power}{RESET}") +
                        right_aligned_format.format(f"Flush:{BRIGHT_GREEN if green_Stocks_profit_loss > 0 else BRIGHT_RED}{round(green_Stocks_profit_loss)}{RESET}"))    
    output_lines.append(left_aligned_format.format(f"Status:{BRIGHT_GREEN if nse_action in ('Bullish', 'Bull') else BRIGHT_RED}{nse_action}{RESET}") +
                        right_aligned_format.format(f"Booked:{BRIGHT_GREEN if result > 0 else BRIGHT_RED}{round(result)}{RESET}"))
          
    output_lines.append("-" * 42)     
    output_lines.append(f'{BRIGHT_YELLOW}🏛🏛 PXY® PreciseXceleratedYield Pvt Ltd™ 🏛🏛{RESET}')
    output_lines.append("-" * 42)
    #output_lines.append(f"{BRIGHT_YELLOW}Market is {nse_action} ⚡💥 - Power⚡💥{nse_power}{RESET}💥⚡")
    # Join the lines to create the full output
    full_output = '\n'.join(output_lines)
    # Print to console
    print(full_output)
    # Write to file
    with open("bordpxy.txt", "w") as file:
        file.write(full_output)
