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
###########################################################################################################################################################################################################    
    import pandas as pd
    # Assuming you have a list of instrument keys, e.g., ['NIFTY50', 'RELIANCE', ...]
    instrument_keys = ['NSE:NIFTY 50']
    # Create an empty DataFrame named NIFTY
    NIFTY = pd.DataFrame()
    # Get OHLC data for the list of keys
    resp = broker.kite.ohlc("NSE:NIFTY 50")
    # Create a dictionary from the response for easier mapping
    dct = {
        k: {
            'ltp': v['ohlc'].get('ltp', v['last_price']),
            'open': v['ohlc']['open'],
            'high': v['ohlc']['high'],
            'low': v['ohlc']['low'],
            'close_price': v['ohlc']['close'],
        }
        for k, v in resp.items()
    }
    # Set the 'key' column to the instrument keys from your list
    NIFTY['key'] = instrument_keys
    # Populate other columns based on the dct dictionary
    NIFTY['ltp'] = NIFTY['key'].map(lambda x: dct.get(x, {}).get('ltp', 0))
    NIFTY['timestamp'] = pd.to_datetime('now').strftime('%H:%M:%S')
    NIFTY['open'] = NIFTY['key'].map(lambda x: dct.get(x, {}).get('open', 0))
    NIFTY['high'] = NIFTY['key'].map(lambda x: dct.get(x, {}).get('high', 0))
    NIFTY['low'] = NIFTY['key'].map(lambda x: dct.get(x, {}).get('low', 0))
    NIFTY['close_price'] = NIFTY['key'].map(lambda x: dct.get(x, {}).get('close_price', 0))
    NIFTY['Day_Change_%'] = round(((NIFTY['ltp'] - NIFTY['close_price']) / NIFTY['close_price']) * 100, 2)
    NIFTY['Open_Change_%'] = round(((NIFTY['ltp'] - NIFTY['open']) / NIFTY['open']) * 100, 2)
    NIFTYconditions = [
        (NIFTY['Day_Change_%'] > 0) & (NIFTY['Open_Change_%'] > 0),
        (NIFTY['Open_Change_%'] > 0) & (NIFTY['Day_Change_%'] < 0),
        (NIFTY['Day_Change_%'] < 0) & (NIFTY['Open_Change_%'] < 0),
        (NIFTY['Day_Change_%'] > 0) & (NIFTY['Open_Change_%'] < 0)
    ]
    choices = ['SuperBull', 'Bull', 'SuperBear', 'Bear']
    NIFTY['Day Status'] = np.select(NIFTYconditions, choices, default='Bear')
    status_factors = {
        'SuperBull': +1,
        'Bull': 0,
        'Bear': 0,
        'SuperBear': -1
    }
    # Calculate 'Score' for each row based on 'Day Status' and 'status_factors'
    NIFTY['Score'] = NIFTY['Day Status'].map(status_factors).fillna(0)
    score_value = NIFTY['Score'].values[0]
    # Assuming you have a DataFrame named "NIFTY" with columns 'ltp', 'low', 'high', 'close'
    # Calculate the metrics
    
    epsilon = 1e-10
    NIFTY['strength']= ((NIFTY['ltp'] - (NIFTY['low'] - 0.01)) / (abs(NIFTY['high'] + 0.01) - abs(NIFTY['low'] - 0.01)))    
    NIFTY['weakness'] = ((NIFTY['ltp'] - (NIFTY['high'] - 0.01)) / (abs(NIFTY['high'] + 0.01) - abs(NIFTY['low'] - 0.01)))
    power = NIFTY['strength'].astype(float).round(2).values[0]

    switch = analyze_stock('^NSEI')
