    import pandas as pd
    
    # Assuming PRINT_df_sorted is your DataFrame
    PRINT_df_sorted = PRINT_df.copy()
    
    # Apply the lambda function to limit 'chks' to 2 characters
    PRINT_df_sorted['TR'] = PRINT_df_sorted['TR'].apply(lambda TR: TR[:2] if isinstance(TR, str) else TR)
    
    # Remove 'BSE:' or 'NSE:' from the 'key' column and limit to 3 characters
    PRINT_df_sorted['key'] = PRINT_df_sorted['key'].str.replace(r'(BSE:|NSE:)', '', regex=True).str[:3]
    
    # Sort the DataFrame by 'PL%' in ascending order
    PRINT_df_sorted = PRINT_df_sorted.sort_values(by='PL%', ascending=True)
    
    # Convert the 'PL%' column to integers
    #PRINT_df_sorted.loc[:, 'PL%'] = PRINT_df_sorted['PL%'].astype(int)
    
    # ANSI escape codes for text coloring
    RESET = "\033[0m"
    BRIGHT_YELLOW = "\033[93m"
    
    # Set the maximum width for all columns
    pd.set_option('display.max_colwidth', 1)  # Adjust the value for your desired width
    
    # Apply truncation to each cell in the DataFrame
    PRINT_df_sorted_display = PRINT_df_sorted.copy()
    print("*" * 42)
    
    # Always print "Table" in bright yellow
    
    
    # Print the truncated DataFrame without color
    # Assuming PRINT_df_sorted_display is your DataFrame
    filtered_df = PRINT_df_sorted_display[PRINT_df_sorted_display['PL%'] > 1.4]
    mis_filtered_df = PRINT_df_sorted_display[PRINT_df_sorted_display['Y'] == 'M']
    mis_filtered_df = mis_filtered_df.sort_values(by='PL%', ascending=False)

    
    print(f"{BRIGHT_YELLOW}Table–CNC Stocks in positions and holdings{RESET}")
    if not filtered_df.empty:
        print(filtered_df.to_string(index=False, justify='left', col_space=-2))

    print(f"{BRIGHT_YELLOW}Table–MIS Stocks in positions and negitive{RESET}")
    if not mis_filtered_df.empty:
        print(mis_filtered_df.to_string(index=False, justify='left', col_space=-2))    

    print("*" * 42)
