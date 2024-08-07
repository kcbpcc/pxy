from rich import print
from rich.table import Table
import textwrap
from clorpxy import GREY

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

# Create a table with a box-style border
table = Table(box="SQUARE")

# Add the column header "PXY® PreciseXceleratedYield Pvt Ltd™"
table.add_column("PXY® PreciseXceleratedYield Pvt Ltd™", style=BOLD, width=width)

# Add the row with the wrapped notice in GREY
table.add_row(f"[{GREY}]{wrapped_notice}[/{GREY}]")

# Display the table without extra space
print(table)
