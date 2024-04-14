import pandas as pd
from asciichartpy import plot

# Read the CSV file into a DataFrame
df = pd.read_csv('acvalue.csv')

# Convert 'date' column to datetime format
df['date'] = pd.to_datetime(df['date'])

# Create ASCII chart
chart = plot(df['acvalue'].tolist(), {'height': 20, 'format': "{:,.2f}"})

# Print ASCII chart
print(chart)
