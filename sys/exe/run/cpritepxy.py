from rich import print
from rich.table import Table
import textwrap

# Copyright Notice
copyright_notice = (
    "The PXY® trading tool and its content are protected by copyright laws and international treaties."
    " All rights reserved by PXY® and Unauthorized use, reproduction, and distribution are strictly prohibited."
    " Infringement may lead to legal action and financial penalties. PXY® is committed to protecting its intellectual property."
)

# Set the desired width
width = 41

# Use textwrap to format the text with a fixed width
wrapped_notice = textwrap.fill(copyright_notice, width, break_long_words=False)

# Create a table
table = Table()

# ANSI escape code for bright yellow color
yellow_color_code = "\033[93m"
reset_color_code = "\033[0m"

# Add a column to the table with the specified header
table.add_column(f"{yellow_color_code}PXY® PreciseXceleratedYield Pvt Ltd™{reset_color_code}", [value1, value2, value3])  # Replace value1, value2, value3 with your actual values


# Add the row with the wrapped notice
table.add_row(wrapped_notice)

# Display the table without extra space
print(table)










