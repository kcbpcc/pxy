import yfinance as yf
import warnings
from fbprophet import Prophet

# Suppress all warnings
warnings.filterwarnings("ignore")

# Fetch Nifty data with 1-minute intervals for the last 5 days
nifty_data = yf.Ticker('^NSEI').history(period="5d", interval="1m")

# Reset index to make Date a column
nifty_data.reset_index(inplace=True)

# Ensure the data is sorted in ascending order by date
nifty_data = nifty_data.sort_values(by='Date')

# Rename columns as required by Prophet
nifty_data.rename(columns={'Date': 'ds', 'Close': 'y'}, inplace=True)

# Initialize Prophet model
model = Prophet()

# Fit the model
model.fit(nifty_data)

# Make future dataframe for 7 minutes ahead
future = model.make_future_dataframe(periods=7, freq='T')

# Forecast
forecast = model.predict(future)

# Get the forecasted values
forecasted_values = forecast[['ds', 'yhat']].tail(7)

# Get the current price
current_price = nifty_data.iloc[-1]['y']

# Compare current price with the forecasted values
for idx, row in forecasted_values.iterrows():
    if current_price > row['yhat']:
        print(f"The current price is above the forecasted value at {row['ds']}.")
    elif current_price < row['yhat']:
        print(f"The current price is below the forecasted value at {row['ds']}.")
    else:
        print(f"The current price is equal to the forecasted value at {row['ds']}.")

