from clorpxy import RED, GREEN, RESET

def format_investments(total_invested_pe, total_invested_ce):
    """
    Formats the total investments in PE and CE options using a 40-character bar
    with color coding based on their ratio and symbol placement based on investment comparison.
    Considers investments equal if the ratio is within a 5% deviation range.
    
    Args:
    total_invested_pe (float): The total investment in PE options.
    total_invested_ce (float): The total investment in CE options.
    
    Returns:
    str: A formatted string with color-coded bars representing the investments.
    """
    # Calculate total investment
    total_investment = total_invested_pe + total_invested_ce
    
    if total_investment == 0:
        return '━' * 38
    
    # Calculate the ratio for PE and CE investments
    pe_ratio = total_invested_pe / total_investment
    ce_ratio = total_invested_ce / total_investment
    
    # Determine if investments are considered equal within a 5% deviation range
    deviation_threshold = 0.05
    if abs(pe_ratio - ce_ratio) <= deviation_threshold:
        symbols = "🥅"
        total_width = 39  # Adjusted width to fit symbols
    elif total_invested_ce > total_invested_pe:
        symbols = "🏃‍➡️⚽"
        total_width = 37  # Adjusted width to fit symbols
    else:
        symbols = "⚽🏃"
        total_width = 37  # Adjusted width to fit symbols
    
    # Determine the number of ━ characters for each investment
    pe_width = int(total_width * pe_ratio)
    ce_width = total_width - pe_width  # Remaining width for CE investment
    
    # Create the formatted bars
    pe_bar = RED + '━' * pe_width + RESET
    ce_bar = GREEN + '━' * ce_width + RESET
    
    # Combine the bars with the divider and symbols
    formatted_output = pe_bar + symbols + ce_bar
    
    return formatted_output
