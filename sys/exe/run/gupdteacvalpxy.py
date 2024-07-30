import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Path to your OAuth 2.0 credentials JSON file in the same directory
CREDS_FILE = 'gupdteacvalpxy.json'

# Define the scope
scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']

# Authenticate and create a client instance
creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS_FILE, scope)
client = gspread.authorize(creds)

# Open the spreadsheet by key
spreadsheet_id = '15WOo4nE8kK-ZjQKdeRpbtHnqwYExFX4w36IiXyLzVyA'
sheet = client.open_by_key(spreadsheet_id).sheet1

# Data to update
values = [
    ['Test1', 'Test2', 'Test3', 'Test4'],
    ['Test5', 'Test6', 'Test7', 'Test8'],
    ['Test9', 'Test10', 'Test11', 'Test12'],
]

# Update the sheet
sheet.update('A1:D3', values)

print("Sheet updated successfully.")
