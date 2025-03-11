from flexpdf.components.table import TableComponent, TableRow, TableHeader, TableCell
from flexpdf.components.col import FlexCol
from flexpdf.components.text import TextComponent
from reportlab.platypus import SimpleDocTemplate
from reportlab.lib.pagesizes import A4, landscape

from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet
styles = getSampleStyleSheet()


# Create PDF
doc = SimpleDocTemplate("test_table_large.pdf", pagesize=landscape(A4))
story = []

# Define a larger table to test page breaks
rows = [
    TableRow([TableHeader("Year", style={"background": "#00ff00", "text_color": "white"}), TableHeader("Jan"), TableHeader("Feb")], 
             style={"background": "#3f51b5", "text_color": "white"})
]

# Add many rows to test page breaking
for i in range(20):
    text = Paragraph("Multiple lines...<br/>"*((i%5)+1), styles["BodyText"])
    
    rows.append(TableRow([
        TableCell(text),  
        TableCell(f"{i}", style={"bold": True}),
        TableCell("Text here too", style={"align": "right", "text_color": "red"})
    ]))


# Create table with page splitting & repeated headers
table = TableComponent(rows, colWidths=[0.2, 0.4, 0.4], repeatHeader=True, breakable=True)
story.append(table)

# Build the PDF
doc.build(story)
print("PDF with large TableComponent generated successfully!")
