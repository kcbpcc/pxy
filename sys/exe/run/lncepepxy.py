from colorpxy import RED, GREEN, RESET

def format_investments(total_invested_pe, total_invested_ce):
    """
    Formats the total investments in PE and CE options using a 40-character bar
    with color coding based on their ratio.
    
    Args:
    total_invested_pe (float): The total investment in PE options.
    total_invested_ce (float): The total investment in CE options.
    
    Returns:
    str: A formatted string with color-coded bars representing the investments.
    """
    # Calculate total investment
    total_investment = total_invested_pe + total_invested_ce
    
    if total_investment == 0:
        return '━' * 40
    
    # Calculate the ratio for PE and CE investments
    pe_ratio = total_invested_pe / total_investment
    ce_ratio = total_invested_ce / total_investment
    
    # Determine the number of ━ characters for each investment
    total_width = 40
    pe_width = int(total_width * pe_ratio)
    ce_width = total_width - pe_width  # Remaining width for CE investment
    
    # Create the formatted bars
    pe_bar = RED + '━' * pe_width + RESET
    ce_bar = GREEN + '━' * ce_width + RESET
    
    # Combine the bars
    formatted_output = pe_bar + ce_bar
    
    return formatted_output
