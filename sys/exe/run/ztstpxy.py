import os
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import plotly.subplots as sp

# Define ticker symbols for Nifty 50 and Bank Nifty
ticker_symbols = {"Nifty 50": "^NSEI", "Bank Nifty": "^NSEBANK"}

# Function to download data
def download_data(ticker, period='1d', interval='1m'):
    data = yf.download(ticker, period=period, interval=interval)
    data.reset_index(inplace=True)
    data.rename(columns={'index': 'Datetime'}, inplace=True)
    return data

# Download data for both indices
nifty_data = download_data(ticker_symbols["Nifty 50"])
banknifty_data = download_data(ticker_symbols["Bank Nifty"])

# Define the CSV file paths
nifty_csv = 'nifty50_1min.csv'
banknifty_csv = 'banknifty_1min.csv'

# Function to combine new data with existing CSV data
def combine_data(new_data, csv_file):
    if os.path.exists(csv_file):
        existing_data = pd.read_csv(csv_file)
        if 'Datetime' not in existing_data.columns:
            print(f"Adding 'Datetime' column to existing data in {csv_file}")
            existing_data['Datetime'] = pd.date_range(end=pd.Timestamp.now(), periods=len(existing_data), freq='min')
        existing_data['Datetime'] = pd.to_datetime(existing_data['Datetime'], utc=True, format='mixed')
        new_data['Datetime'] = pd.to_datetime(new_data['Datetime'], utc=True, format='mixed')
        combined_data = pd.concat([existing_data, new_data]).drop_duplicates(subset='Datetime').reset_index(drop=True)
    else:
        combined_data = new_data
    combined_data.to_csv(csv_file, index=False)
    return combined_data

# Combine data and save to CSV
nifty_combined = combine_data(nifty_data, nifty_csv)
banknifty_combined = combine_data(banknifty_data, banknifty_csv)

# Function to prepare data for plotting
def prepare_data(data, title):
    data['Datetime'] = pd.to_datetime(data['Datetime'], utc=True, format='mixed')
    data.set_index('Datetime', inplace=True)
    data['SMA_50'] = data['Close'].rolling(window=50, min_periods=1).mean()
    return data

# Prepare data for plotting
nifty_combined = prepare_data(nifty_combined, "Nifty 50")
banknifty_combined = prepare_data(banknifty_combined, "Bank Nifty")

# Create subplots
fig = sp.make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Nifty 50 Index", "Bank Nifty Index"))

# Add Nifty 50 data to subplot
fig.add_trace(go.Scatter(x=nifty_combined.index, y=nifty_combined['Close'], mode='lines', name='Nifty 50 Close', showlegend=False), row=1, col=1)
fig.add_trace(go.Scatter(x=nifty_combined.index, y=nifty_combined['SMA_50'], mode='lines', name='Nifty 50 50-Day SMA', showlegend=False), row=1, col=1)

# Add Bank Nifty data to subplot
fig.add_trace(go.Scatter(x=banknifty_combined.index, y=banknifty_combined['Close'], mode='lines', name='Bank Nifty Close', showlegend=False), row=2, col=1)
fig.add_trace(go.Scatter(x=banknifty_combined.index, y=banknifty_combined['SMA_50'], mode='lines', name='Bank Nifty 50-Day SMA', showlegend=False), row=2, col=1)

# Update layout
fig.update_layout(
    title='Nifty 50 and Bank Nifty Indices - 1 Minute Interval with 50-Day SMA',
    xaxis_title='Datetime',
    yaxis_title='Price',
    showlegend=False,  # Hide the legend
    yaxis=dict(side='right'),  # Price axis on the right for the first subplot
    yaxis2=dict(side='right')  # Price axis on the right for the second subplot
)

# Disable range slider
fig.update_xaxes(rangeslider_visible=False)

# Save the plot to an HTML file
html_file = 'nifty_and_banknifty_1min.html'
fig.write_html(html_file)

# Inject auto-refresh JavaScript
with open(html_file, 'r') as file:
    html_content = file.read()

refresh_script = """
<script>
    setTimeout(function(){
       window.location.reload(1);
    }, 60000);  // Refresh every 60 seconds
</script>
"""

html_content = html_content.replace("</body>", refresh_script + "</body>")

with open(html_file, 'w') as file:
    file.write(html_content)

print(f"CSV files saved as: {nifty_csv}, {banknifty_csv}")
print(f"HTML file saved as: {html_file}")
