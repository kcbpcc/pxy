import re
import datetime
import pytz
from oauth2client.service_account import ServiceAccountCredentials
import gspread

def parse_text_to_table(text):
    # Remove color codes
    text = remove_color_codes(text)
    
    # Split the text into lines
    lines = text.strip().split('\n')
    
    # Initialize an empty table
    table = []
    
    # Iterate over each line
    for line in lines:
        # Split the line based on the occurrence of "  " (double space)
        parts = line.split("  ")
        
        # Check if "PXY®" is present in the second part
        if "PXY®" in parts[1]:
            # If "PXY®" is present, split the second part based on "PXY®" and keep the first part
            part_1 = parts[1].split("PXY®")[0]
            part_2 = "PXY®"
            part_3 = "↑"  # Assuming "↑" is always present
        else:
            # If "PXY®" is not present, keep the second part as it is
            part_1 = parts[1]
            part_2 = ""
            part_3 = ""
        
        # Append the parsed parts to the table
        table.append([parts[0], part_1.strip(), part_2.strip() + part_3.strip(), parts[2]])
    
    return table

def remove_color_codes(text):
    # Define the color codes to be removed
    color_codes = ['[92m', '[91m', '[93m', '[90m', '[1m', '[4m', '[0m']
    
    # Remove color codes
    for code in color_codes:
        text = text.replace(code, '')
    
    return text

def update_google_sheet(table):
    # Load Google Sheets credentials from a service account file
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('accvalue.json', scope)
    client = gspread.authorize(credentials)

    # Open the Google Sheet
    sheet = client.open("dashboard").sheet1  # Replace "dashboard" with the actual name of your Google Sheet

    # Clear existing content from the sheet
    sheet.clear()

    # Update the Google Sheet with the table data
    for row_index, row in enumerate(table):
        for col_index, value in enumerate(row):
            sheet.update_cell(row_index + 1, col_index + 1, value)

    print("Google Sheet updated successfully")

def main():
    input_text = """
    Funds:[92m099215[0m                  Delta:[91m-69999[0m
    Real-P&L:[92m4.3[0m                 Run-P&L:[91m-1.27[0m
    Capital:[93m18.51[92m      [1m[4mPXY[0m[92m[90m[1m[4m®[0m↑       Value:[93m017.8[0m
    Postions:[91m0[0m                     Day-P&L:[92m457[0m
    Extras:[92m00000[0m                  BOOKED:[91m00000[0m
    """

    # Parse the input text into a table format
    table = parse_text_to_table(input_text)

    # Update Google Sheet with the parsed table data
    update_google_sheet(table)

if __name__ == "__main__":
    main()

