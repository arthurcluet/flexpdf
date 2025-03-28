from reportlab.platypus import Flowable, Table, TableStyle
from flexpdf.components.base import Component
from reportlab.lib import colors
from flexpdf.components.text import TextComponent
from flexpdf.components.col import FlexCol
from flexpdf.components.row import FlexRow
from reportlab.platypus import KeepTogether
from reportlab.platypus import PageBreak
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet

class TableCell:
    """Represents a single table cell with customizable styles and alignment."""

    def __init__(self, content, style=None):
        """
        :param content: The text or a Paragraph inside the cell.
        :param style: Dictionary with styles like {"bold": True, "text_color": "black", "align": "right"}.
        """
        self.content = content
        self.style = style or {}

    def get_content(self):
        """Returns properly formatted content for ReportLab's Table."""
        return self.content  # No processing needed since we enforce valid types


class TableHeader(TableCell):
    """Represents a header cell with default bold style."""
    def __init__(self, content, style=None):
        default_style = {"bold": True, "text_color": colors.white, "background": "#3f51b5"}
        combined_style = {**default_style, **(style or {})}
        super().__init__(content, combined_style)

class TableRow:
    """Represents a single row of a table."""
    def __init__(self, cells, style=None):
        """
        :param cells: List of TableCell or TableHeader objects.
        :param style: Optional row-level styles.
        """
        self.cells = cells
        self.style = style or {}

class TableComponent(Component):
    """A table component that supports automatic page breaks and repeating headers."""

    def __init__(self, rows, colWidths=None, repeatHeader=True, breakable=True, style=None):
        """
        :param rows: List of TableRow objects.
        :param colWidths: List of relative column widths (e.g., [0.3, 0.4, 0.3]).
        :param repeatHeader: If True, repeats the first row as a header on new pages.
        :param breakable: If True, allows table splitting across pages.
        :param style: Custom styles for the table (borders, spacing).
        """
        super().__init__(style)
        self.rows = rows
        self.colWidths = colWidths or [1 / len(rows[0].cells)] * len(rows[0].cells)
        self.repeatHeader = repeatHeader
        self.breakable = breakable
        self.table = None

    def wrap(self, availWidth, availHeight):
        """Prepares the table, ensuring it fits inside the available space."""
        column_widths = [availWidth * w for w in self.colWidths]

        # Convert TableRow objects to a list of cell contents
        # Convert TableRow objects into table data
        # Convert TableRow objects into table data
        
        # Convert TableRow objects into table data
        table_data = [[cell.get_content() for cell in row.cells] for row in self.rows]


        # Create Table
        self.table = Table(table_data, colWidths=column_widths)

        # Apply styles
        self.apply_table_styles()

        self.width, self.height = self.table.wrap(availWidth, availHeight)
        return self.width, self.height

    def apply_table_styles(self):
        """Ensures that individual TableHeader or TableCell styles are prioritized over row styles, including alignment."""
        styles = [
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),  # Keep borders
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')  # Default vertical alignment
        ]

        # Apply header styles if repeatHeader=True
        if self.repeatHeader:
            for col in range(len(self.rows[0].cells)):  # Apply to header row only
                header_cell = self.rows[0].cells[col]
                if isinstance(header_cell, TableHeader):
                    bg_color = header_cell.style.get("background", colors.HexColor("#3f51b5"))
                    text_color = header_cell.style.get("text_color", colors.white)
                    styles.append(('BACKGROUND', (col, 0), (col, 0), bg_color))
                    styles.append(('TEXTCOLOR', (col, 0), (col, 0), text_color))

        # Apply row styles while ensuring individual TableHeader styles are not overridden
        for row_idx, row in enumerate(self.rows):
            row_bg = row.style.get("background", None)
            row_text_color = row.style.get("text_color", None)

            for col_idx, cell in enumerate(row.cells):
                if isinstance(cell, TableHeader):  # Prioritize TableHeader styles
                    continue  # Skip because it's already styled

                # Apply row background color **only if cell doesn't have its own**
                if row_bg and "background" not in cell.style:
                    styles.append(('BACKGROUND', (col_idx, row_idx), (col_idx, row_idx), row_bg))

                # Apply row text color **only if cell doesn't have its own**
                if row_text_color and "text_color" not in cell.style:
                    styles.append(('TEXTCOLOR', (col_idx, row_idx), (col_idx, row_idx), row_text_color))

                # **New: Apply individual cell alignment (if set)**
                cell_align = cell.style.get("align", "left")  # Default to left alignment
                align_map = {"left": "LEFT", "center": "CENTER", "right": "RIGHT"}
                if cell_align in align_map:
                    styles.append(('ALIGN', (col_idx, row_idx), (col_idx, row_idx), align_map[cell_align]))

        self.table.setStyle(TableStyle(styles))





        
    def split(self, availWidth, availHeight):
        """Splits the table correctly, ensuring the header appears only at the start of new pages."""
        if not self.breakable:
            return []

        # Convert TableRow objects into raw table data
        table_data = [[cell.get_content() for cell in row.cells] for row in self.rows]

        # Create a temporary table to measure actual row heights
        temp_table = Table(table_data, colWidths=[availWidth * w for w in self.colWidths])

        # Get row heights dynamically
        _, total_height = temp_table.wrap(availWidth, availHeight)
        row_heights = temp_table._rowHeights  

        space_used = 0
        split_at = None

        # Find where to break the table
        for i, height in enumerate(row_heights):
            if space_used + height > availHeight:
                split_at = i
                break
            space_used += height

        if split_at is None or split_at == 0:
            return []  # Everything fits, no need to split

        # First part that fits on the current page
        first_part = self.rows[:split_at]
        second_part = self.rows[split_at:]

        # **Fix: Always insert the header at the top of the new page if repeatHeader=True**
        if self.repeatHeader and second_part and isinstance(self.rows[0].cells[0], TableHeader):
            second_part.insert(0, self.rows[0])  # Insert header row at the top

        return [
            TableComponent(first_part, self.colWidths, self.repeatHeader, self.breakable),
            PageBreak(),  # Ensure the next part starts on a new page
            TableComponent(second_part, self.colWidths, self.repeatHeader, self.breakable)
        ]


    def draw(self):
        """Delegates drawing to the wrapped Table."""
        if self.table:
            self.table.drawOn(self.canv, 0, 0)
