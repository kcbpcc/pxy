import pandas as pd
import yfinance as yf

def heikin_ashi(df):
    ha_df = df.copy()
    ha_df['HA_Close'] = (df['Open'] + df['High'] + df['Low'] + df['Close']) / 4
    ha_df['HA_Open'] = 0.0
    ha_df['HA_High'] = 0.0
    ha_df['HA_Low'] = 0.0

    for i in range(len(df)):
        if i == 0:
            ha_df.at[ha_df.index[i], 'HA_Open'] = (df['Open'].iloc[i] + df['Close'].iloc[i]) / 2
        else:
            ha_df.at[ha_df.index[i], 'HA_Open'] = (ha_df['HA_Open'].iloc[i-1] + ha_df['HA_Close'].iloc[i-1]) / 2
        ha_df.at[ha_df.index[i], 'HA_High'] = max(df['High'].iloc[i], ha_df['HA_Open'].iloc[i], ha_df['HA_Close'].iloc[i])
        ha_df.at[ha_df.index[i], 'HA_Low'] = min(df['Low'].iloc[i], ha_df['HA_Open'].iloc[i], ha_df['HA_Close'].iloc[i])
    
    return ha_df

# Read the CSV file containing the NSE codes
csv_file = 'bankspxy.csv'
df = pd.read_csv(csv_file)

# Assuming the CSV file has a single column with header 'NSE Code'
nse_codes = df['NSE Code'].tolist()

# Dictionary to store current prices and Heikin-Ashi status
current_prices = {}
ha_status = {}

# Fetch historical prices and calculate Heikin-Ashi for each NSE code
for code in nse_codes:
    ticker = f"{code}.NS"  # Append .NS to indicate NSE
    stock = yf.Ticker(ticker)
    history = stock.history(period='5d')  # Fetch last 5 days to get yesterday's data

    if not history.empty:
        ha_df = heikin_ashi(history)
        yesterday_ha = ha_df.iloc[-2]
        today_ha = ha_df.iloc[-1]
        
        # Check if yesterday was red and today is green
        if yesterday_ha['HA_Close'] < yesterday_ha['HA_Open'] and today_ha['HA_Close'] > today_ha['HA_Open']:
            current_prices[code] = history['Close'].iloc[-1]
            ha_status[code] = "Red HA yesterday, Green HA today"

# Print the current prices and Heikin-Ashi status
for code, price in current_prices.items():
    print(f"{code}: {price}, Status: {ha_status[code]}")
