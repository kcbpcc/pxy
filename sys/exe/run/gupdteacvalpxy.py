import gspread

# Use gspread's client without OAuth
client = gspread.client.Client(None)

# Open the spreadsheet by its key
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

