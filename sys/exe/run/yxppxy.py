###########################################################################################################################################################################################################
    epsilon = 1e-10
    
    combined_df[['strength', 'weakness']] = combined_df.apply(
        lambda row: pd.Series({
            'strength': round((row['ltp'] - (row['low'] - 0.01)) / (abs(row['high'] + 0.01) - abs(row['low'] - 0.01) + epsilon) if (abs(row['high'] + 0.01) - abs(row['low'] - 0.01) + epsilon != 0) and (row['ltp'] - (row['low'] - 0.01) != 0) else 0.5, 2),
            'weakness': round((row['ltp'] - (row['high'] + 0.01)) / (abs(row['high'] + 0.01) - abs(row['low'] - 0.01) + epsilon) if (abs(row['high'] + 0.01) - abs(row['low'] - 0.01) + epsilon != 0) and (row['ltp'] - (row['high'] + 0.01) != 0) else 0.5, 2)
        }), axis=1
    )
    
    combined_df[['pr', 'xl', 'yi', '_pr', '_xl', '_yi']] = combined_df.apply(
        lambda row: pd.Series({
            'pr': round(max(0.4, round(0.0 + (row['strength'] * 1.0), 2) * 1 - epsilon), 2),
            'xl': round(max(0.8, round(0.0 + (row['strength'] * 1.0), 2) * 1.5 - epsilon), 2),
            'yi': round(max(1.2, round(0.0 + (row['strength'] * 1.0), 2) * 2 - epsilon), 2),
            '_pr': round(min(-0.3, round(0.0 + (row['weakness'] * 1.0), 2) * 0.3 - epsilon), 2),
            '_xl': round(min(-0.6, round(0.0 + (row['weakness'] * 1.0), 2) * 0.6 - epsilon), 2),
            '_yi': round(min(-1.0, round(0.0 + (row['weakness'] * 1.0), 2) * 1.0 - epsilon), 2),
        }), axis=1
    )
    
    def calculate_pxy(row):
        smbchk = row['smbchk']
        pr, xl, yi = row['pr'], row['xl'], row['yi']
    
        if smbchk == "Bear": 
            return round(max(pr, pr), 2)
            
        elif smbchk == "Buy": 
            return round(max(pr, yi), 2)

        elif smbchk == "Bull":
            return round(max(pr, yi), 2)

        elif smbchk == "Sell":
            return round(max(pr, xl), 2)
        
        else:
            return round(pr, 2)
    
    def calculate_yxp(row):
        smbchk = row['smbchk']
        _pr, _xl, _yi = row['_pr'], row['_xl'], row['_yi']
    
        if smbchk == "Bear":
            return round(min(_pr, _yi), 2)
    
        elif smbchk == "Buy":
            return round(min(_pr, _xl), 2)
    
        elif smbchk == "Bull":
            return round(min(_pr, _pr), 2)
    
        elif smbchk == "Sell":
            return round(min(_pr, _yi), 2)
    
        else:
            return round(_pr, 2)

    
    combined_df['pxy'] = combined_df.apply(calculate_pxy, axis=1)
    combined_df['yxp'] = combined_df.apply(calculate_yxp, axis=1)
