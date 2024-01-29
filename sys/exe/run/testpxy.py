import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

def calculate_macd(data, short_window=12, long_window=26, signal_window=9):
    # Calculate Short Term Exponential Moving Average
    short_ema = data['Close'].ewm(span=short_window, adjust=False).mean()
    
    # Calculate Long Term Exponential Moving Average
    long_ema = data['Close'].ewm(span=long_window, adjust=False).mean()
    
    # Calculate MACD line
    data['MACD'] = short_ema - long_ema
    
    # Calculate Signal line
    data['Signal_Line'] = data['MACD'].ewm(span=signal_window, adjust=False).mean()
    
    # Calculate MACD Histogram
    data['MACD_Histogram'] = data['MACD'] - data['Signal_Line']

    return data

# Download TCS data
symbol = 'TCS.BO'  # TCS stock on BSE, change to 'TCS' for NSE
tcs_data = yf.download(symbol, start='2022-01-01', end='2023-01-01')

# Check if 'dst_error_hours' column is present
if 'dst_error_hours' in tcs_data.columns:
    # Address FutureWarning
    tcs_data.index += pd.to_timedelta(tcs_data['dst_error_hours'], 'h')
    tcs_data = tcs_data.drop('dst_error_hours', axis=1)

# Calculate MACD
tcs_data = calculate_macd(tcs_data)

# Plotting the data
plt.figure(figsize=(10, 6))
plt.plot(tcs_data['Close'], label='TCS Close Price', linewidth=2)
plt.plot(tcs_data['MACD'], label='MACD Line', linestyle='--', color='orange')
plt.plot(tcs_data['Signal_Line'], label='Signal Line', linestyle='--', color='green')
plt.bar(tcs_data.index, tcs_data['MACD_Histogram'], label='MACD Histogram', color='gray', alpha=0.5)

plt.title('TCS Stock Price and MACD')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()
plt.show()



