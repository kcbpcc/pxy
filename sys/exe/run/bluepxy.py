import yfinance as yf
import pandas as pd
import numpy as np
from statsmodels.tsa.statespace.sarimax import SARIMAX
import matplotlib.pyplot as plt

# Fetch Nifty data with 1-minute intervals
nifty_data = yf.download('^NSEI', start='2020-01-01', end='2024-01-01', interval='1m')

# Keep only 'Close' prices
nifty_close = nifty_data['Close'].dropna()

# Fit SARIMA model
model = SARIMAX(nifty_close, order=(1, 1, 1), seasonal_order=(1, 1, 1, 12))  # Example order, tune as needed
fit_model = model.fit(disp=False)

# Forecast 7 periods ahead (7 minutes)
forecast = fit_model.forecast(steps=7)

# Get the current price
current_price = nifty_close.iloc[-1]

# Compare current price with the forecasted values
for idx, forecasted_price in enumerate(forecast):
    if current_price > forecasted_price:
        print(f"The current price is above the forecasted value at {nifty_close.index[-1] + pd.Timedelta(minutes=(idx + 1))}.")
    elif current_price < forecasted_price:
        print(f"The current price is below the forecasted value at {nifty_close.index[-1] + pd.Timedelta(minutes=(idx + 1))}.")
    else:
        print(f"The current price is equal to the forecasted value at {nifty_close.index[-1] + pd.Timedelta(minutes=(idx + 1))}.")

