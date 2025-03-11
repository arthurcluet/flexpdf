from reportlab.platypus import Flowable, Table, TableStyle
from flexpdf.components.base import Component
from reportlab.lib import colors

class FlexCol(Component):
    """A column-like flex container that stacks elements vertically with gaps and allows page breaks."""
    
    def __init__(self, elements, gap=10, breakable=True, style=None):
        """
        :param elements: List of Flowable elements.
        :param gap: Space (in points) between elements.
        :param breakable: If True, allows page breaks when content is too large.
        :param style: Custom styles (borders, padding, etc.).
        """
        super().__init__(style)
        self.elements = elements
        self.gap = gap
        self.breakable = breakable
        self.table = None

    def wrap(self, availWidth, availHeight):
        """Computes total height dynamically, ensuring it fits parent width."""
        row_data = []
        row_heights = []
        total_height = 0

        self.split_index = None  # Where to break for a new page

        # Insert each element into its own row, adding gaps in between
        for i, element in enumerate(self.elements):
            h = element.wrap(availWidth, availHeight)[1]  # Get element height
            if self.breakable and total_height + h > availHeight:  # If breakable and exceeds page, split
                self.split_index = i
                break
            elif not self.breakable and total_height + h > availHeight:  # If not breakable, force overflow
                raise ValueError("FlexCol is too large and is not allowed to break across pages.")

            row_data.append([element])  # Add element in its row
            row_heights.append(h)
            total_height += h

            if i < len(self.elements) - 1:
                row_data.append([""])  # Empty row for gap
                row_heights.append(self.gap)
                total_height += self.gap

        # Create the Table structure
        self.table = Table(row_data, colWidths=[availWidth], rowHeights=row_heights)

        # Apply styling (optional)
        self.table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ]))

        # Get actual width and height after wrapping
        self.width, self.height = self.table.wrap(availWidth, availHeight)
        return self.width, self.height

    def split(self, availWidth, availHeight):
        """Breaks the column into multiple parts when needed."""
        if not self.breakable or self.split_index is None:
            return []

        # Create a new FlexCol with the remaining elements
        remaining_elements = self.elements[self.split_index:]
        return [FlexCol(remaining_elements, self.gap, self.breakable)]

    def draw(self):
        """Delegates drawing to the internally wrapped Table."""
        if self.table:
            self.table.drawOn(self.canv, 0, 0)
