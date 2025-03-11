from reportlab.platypus import Flowable, Table, TableStyle
from flexpdf.components.base import Component  # Import base class
from reportlab.lib import colors

class FlexRow(Component):
    """A row-like flex container that distributes elements horizontally with gaps."""

    def __init__(self, elements, widths, gap=5, style=None):
        """
        :param elements: List of Flowable elements.
        :param widths: List of relative widths (e.g., [0.4, 0.6]).
        :param gap: Space (in points) between elements.
        :param style: Custom styles (borders, padding, etc.).
        """
        super().__init__(style)
        self.elements = elements
        self.widths = widths
        self.gap = gap
        self.table = None

        assert len(elements) == len(widths), "Elements and widths must match"
        assert sum(widths) == 1.0, "Widths must sum to 1 (100%)"

    def wrap(self, availWidth, availHeight):
        """Dynamically calculate exact widths considering gaps."""
        num_gaps = len(self.widths) - 1  # Number of gaps between elements
        total_gap_width = self.gap * num_gaps  # Total space used by gaps

        # Compute available width after accounting for gaps
        total_available_width = availWidth - total_gap_width
        colWidths = [(w * total_available_width) for w in self.widths]  # Scale widths

        # Create row layout: Insert gaps as empty columns
        row_data = []
        for i, element in enumerate(self.elements):
            row_data.append(element)  # Add element
            if i < num_gaps:
                row_data.append("")  # Add empty cell for gap

        # Create the final column widths array (including gaps)
        final_colWidths = []
        for i, w in enumerate(colWidths):
            final_colWidths.append(w)  # Add computed width
            if i < num_gaps:
                final_colWidths.append(self.gap)  # Add gap width

        # Create the internal Table
        self.table = Table([row_data], colWidths=final_colWidths)

        # Apply styles
        self.table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),  # Light grid for debugging
        ]))

        # Get actual size
        self.width, self.height = self.table.wrap(availWidth, availHeight)
        return self.width, self.height

    def draw(self):
        """Delegates drawing to the internally wrapped Table."""
        if self.table:
            self.table.drawOn(self.canv, 0, 0)
