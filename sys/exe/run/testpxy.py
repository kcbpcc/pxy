# Given values
row = {'smbchk': '', 'pr': 1, 'xl': 2, 'yi': 3, '_pr': -1, '_xl': -2, '_yi': -3}

# Evaluate Buy
row['smbchk'] = 'Buy'
pxy_buy = calculate_pxy(row)
yxp_buy = calculate_yxp(row)
print("Buy - pxy:", pxy_buy, "yxp:", yxp_buy)

# Evaluate Bull
row['smbchk'] = 'Bull'
pxy_bull = calculate_pxy(row)
yxp_bull = calculate_yxp(row)
print("Bull - pxy:", pxy_bull, "yxp:", yxp_bull)

# Evaluate Sell
row['smbchk'] = 'Sell'
pxy_sell = calculate_pxy(row)
yxp_sell = calculate_yxp(row)
print("Sell - pxy:", pxy_sell, "yxp:", yxp_sell)

# Evaluate Bear
row['smbchk'] = 'Bear'
pxy_bear = calculate_pxy(row)
yxp_bear = calculate_yxp(row)
print("Bear - pxy:", pxy_bear, "yxp:", yxp_bear)

