import os
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# Define the ticker symbol for Nifty 50
ticker_symbol = "^NSEI"

# Fetch the new data
new_data = yf.download(ticker_symbol, period='1d', interval='1m')

# Ensure the column names are standardized
new_data.reset_index(inplace=True)
new_data.rename(columns={'index': 'Datetime'}, inplace=True)

# Define the CSV file path
csv_file = 'nifty50_1min.csv'

# Function to debug column names
def print_column_names(df, name):
    print(f"Columns in {name}: {df.columns.tolist()}")

if os.path.exists(csv_file):
    # Read the existing data
    existing_data = pd.read_csv(csv_file)

    # Debug: Print column names
    print_column_names(existing_data, 'existing_data')

    # Check if 'Datetime' column is missing and add it
    if 'Datetime' not in existing_data.columns:
        print("Adding 'Datetime' column to existing data")
        existing_data['Datetime'] = pd.date_range(end=pd.Timestamp.now(), periods=len(existing_data), freq='T')
    
    # Ensure the 'Datetime' column is in datetime format
    existing_data['Datetime'] = pd.to_datetime(existing_data['Datetime'])

    # Ensure the 'Datetime' column in the new data is in datetime format
    new_data['Datetime'] = pd.to_datetime(new_data['Datetime'])

    # Concatenate the new data with the existing data, keeping only unique records
    combined_data = pd.concat([existing_data, new_data]).drop_duplicates(subset='Datetime').reset_index(drop=True)
else:
    # If the CSV file does not exist, use the new data as the combined data
    combined_data = new_data

# Save the combined data back to the CSV file
combined_data.to_csv(csv_file, index=False)

# Debug: Print column names
print_column_names(combined_data, 'combined_data')

# Read the CSV file for plotting
data = pd.read_csv(csv_file)

# Ensure the 'Datetime' column is in datetime format
data['Datetime'] = pd.to_datetime(data['Datetime'])
data.set_index('Datetime', inplace=True)

# Calculate the 50-day SMA
data['SMA_50'] = data['Close'].rolling(window=50, min_periods=1).mean()

# Create a plot
fig = go.Figure()

# Add the line for the close prices
fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', name='Close'))

# Add the line for the 50-day SMA
fig.add_trace(go.Scatter(x=data.index, y=data['SMA_50'], mode='lines', name='50-Day SMA'))

# Update the layout
fig.update_layout(
    title='Nifty 50 Index - 1 Minute Interval with 50-Day SMA',
    xaxis_title='Datetime',
    yaxis_title='Price',
    xaxis_rangeslider_visible=True
)

# Save the plot to an HTML file
html_file = 'nifty50_1min.html'
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

print(f"CSV file saved as: {csv_file}")
print(f"HTML file saved as: {html_file}")

