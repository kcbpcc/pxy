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

# Create subplots with minimal vertical spacing
fig = sp.make_subplots(
    rows=2, 
    cols=1, 
    shared_xaxes=True,
    vertical_spacing=0.05  # Adjust vertical spacing between subplots
)

# Add Nifty 50 data to subplot with dark gray colors
fig.add_trace(go.Scatter(x=nifty_combined.index, y=nifty_combined['Close'], mode='lines', name='Nifty 50 Close', line=dict(color='dimgray')), row=1, col=1)
fig.add_trace(go.Scatter(x=nifty_combined.index, y=nifty_combined['SMA_50'], mode='lines', name='Nifty 50 50-Day SMA', line=dict(color='gray')), row=1, col=1)

# Add Bank Nifty data to subplot with dark gray colors
fig.add_trace(go.Scatter(x=banknifty_combined.index, y=banknifty_combined['Close'], mode='lines', name='Bank Nifty Close', line=dict(color='dimgray')), row=2, col=1)
fig.add_trace(go.Scatter(x=banknifty_combined.index, y=banknifty_combined['SMA_50'], mode='lines', name='Bank Nifty 50-Day SMA', line=dict(color='gray')), row=2, col=1)

# Update layout with black background, unified colors, and additional padding
fig.update_layout(
    title='Nifty 50 and Bank Nifty Indices - 1 Minute Interval with 50-Day SMA',
    title_font=dict(size=16, color="gray"),
    showlegend=False,  # Hide the legend
    yaxis=dict(
        side='left',  # Shift Y-axis to the left
        range=[nifty_combined['Close'].min() - 20, nifty_combined['Close'].max() + 20],  # Added padding for y-axis
        showgrid=False,  # Hide grid lines
        showline=True,  # Show y-axis line
        linecolor='gray',  # Color of the y-axis line
        linewidth=1  # Width of the y-axis line
    ),
    yaxis2=dict(
        side='left',  # Shift Y-axis to the left
        range=[banknifty_combined['Close'].min() - 20, banknifty_combined['Close'].max() + 20],  # Added padding for y-axis
        showgrid=False,  # Hide grid lines
        showline=True,  # Show y-axis line
        linecolor='gray',  # Color of the y-axis line
        linewidth=1  # Width of the y-axis line
    ),
    xaxis=dict(
        showgrid=False,  # Hide grid lines
        showline=True,  # Show x-axis line
        title='',         # Hide x-axis title
        tickvals=[],      # Hide x-axis tick labels
        linecolor='gray',  # Color of the x-axis line
        linewidth=1  # Width of the x-axis line
    ),
    xaxis2=dict(
        showgrid=False,  # Hide grid lines
        showline=True,  # Show x-axis line
        title='',         # Hide x-axis title
        tickvals=[],      # Hide x-axis tick labels
        linecolor='gray',  # Color of the x-axis line
        linewidth=1  # Width of the x-axis line
    ),
    paper_bgcolor='black',  # Background color of the entire figure
    plot_bgcolor='black',   # Background color of the plotting area
    font_color='gray',      # Color of the text
    margin=dict(t=50, b=50, l=50, r=50),  # Adjust margins to reduce padding
)

# Add annotations for titles at the bottom of each subplot with gray color
fig.add_annotation(
    text="Nifty 50 Index",
    xref="paper", yref="paper",
    x=0.5, y=0.02,  # Adjust y position for the title at the bottom
    showarrow=False,
    font=dict(size=14, color="gray"),
    align="center",
    bgcolor='black'  # Match background color
)

fig.add_annotation(
    text="Bank Nifty Index",
    xref="paper", yref="paper",
    x=0.5, y=0.48,  # Adjust y position for the title at the bottom
    showarrow=False,
    font=dict(size=14, color="gray"),
    align="center",
    bgcolor='black'  # Match background color
)

# Disable range slider
fig.update_xaxes(rangeslider_visible=False)

# Save the plot to an HTML file
html_file = 'webchrtpxy.html'
fig.write_html(html_file)

# Inject auto-refresh JavaScript and set the body background color to black
with open(html_file, 'r') as file:
    html_content = file.read()

refresh_script = """
<script>
    setTimeout(function(){
       window.location.reload(1);
    }, 60000);  // Refresh every 60 seconds
</script>
"""

# Add inline CSS to set body background color and header color
css_style = """
<style>
    body {
        background-color: black;
    }
    .header {
        color: gray;
    }
</style>
"""

html_content = html_content.replace("</head>", css_style + "</head>")
html_content = html_content.replace("</body>", refresh_script + "</body>")

with open(html_file, 'w') as file:
    file.write(html_content)

print(f"CSV files saved as: {nifty_csv}, {banknifty_csv}")
print(f"HTML file saved as: {html_file}")
