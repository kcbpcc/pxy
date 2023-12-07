# Values
row_buy = {'smbchk': 'Buy', 'pr': 1, 'xl': 2, 'yi': 3, '_pr': -1, '_xl': -2, '_yi': -3}
row_bull = {'smbchk': 'Bull', 'pr': 1, 'xl': 2, 'yi': 3, '_pr': -1, '_xl': -2, '_yi': -3}
row_sell = {'smbchk': 'Sell', 'pr': 1, 'xl': 2, 'yi': 3, '_pr': -1, '_xl': -2, '_yi': -3}
row_bear = {'smbchk': 'Bear', 'pr': 1, 'xl': 2, 'yi': 3, '_pr': -1, '_xl': -2, '_yi': -3}

# Calculate and print results in a table
print("| smbchk | pxy  | yxp  |")
print("|--------|------|------|")

# Buy
pxy_buy = calculate_pxy(row_buy)
yxp_buy = calculate_yxp(row_buy)
print(f"| Buy    | {pxy_buy}  | {yxp_buy}  |")

# Bull
pxy_bull = calculate_pxy(row_bull)
yxp_bull = calculate_yxp(row_bull)
print(f"| Bull   | {pxy_bull}  | {yxp_bull}  |")

# Sell
pxy_sell = calculate_pxy(row_sell)
yxp_sell = calculate_yxp(row_sell)
print(f"| Sell   | {pxy_sell}  | {yxp_sell}  |")

# Bear
pxy_bear = calculate_pxy(row_bear)
yxp_bear = calculate_yxp(row_bear)
print(f"| Bear   | {pxy_bear}  | {yxp_bear}  |")
