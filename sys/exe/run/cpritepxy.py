from rich import print
from rich.table import Table
import textwrap
from clorpxy import SILVER, UNDERLINE, RED, GREEN, YELLOW, RESET, BRIGHT_YELLOW, BRIGHT_RED, BRIGHT_GREEN, BOLD, GREY

# Copyright Notice
copyright_notice = (
    "The PXY® trading tool and its content are protected by copyright laws and international treaties."
    " All rights reserved by PXY® and Unauthorized use, reproduction, and distribution are strictly prohibited."
    " Infringement may lead to legal action and financial penalties. PXY® is committed to protecting its intellectual property."
)

# Set the desired width
width = 38

# Use textwrap to format the text with a fixed width
wrapped_notice = textwrap.fill(copyright_notice, width, break_long_words=False)

# Create a table with dim border and text color
table = Table(border_style="dim")

# Add the column header "PXY® PreciseXceleratedYield Pvt Ltd™" in gray color
table.add_column("PXY® PreciseXceleratedYield Pvt Ltd™", style="dim")

# Add the row with the wrapped notice in gray color
table.add_row(wrapped_notice, style="dim")

# Display the table without extra space
print(table)

