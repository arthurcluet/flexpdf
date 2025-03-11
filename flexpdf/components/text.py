from reportlab.platypus import Flowable, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from flexpdf.components.base import Component
from reportlab.lib import colors

class TextComponent(Component):
    """A text component that supports styling (like an HTML <p> tag)."""

    def __init__(self, text, style=None):
        """
        :param text: The text content.
        :param style: A dictionary of styles (font size, bold, color, etc.).
        """
        super().__init__(style)
        self.text = text
        self.styles = getSampleStyleSheet()
        self.paragraph = None  # Will be created in wrap()

    def wrap(self, availWidth, availHeight):
        """Wraps the text to fit the available width."""
        # Extract styles
        font_size = self.style.get("font_size", 12)
        font_weight = "bold" if self.style.get("bold") else "normal"
        font_color = self.style.get("text_color", colors.black)
        align = self.style.get("align", "left")

        # Create a style for the text
        text_style = self.styles["BodyText"]
        text_style.fontSize = font_size
        text_style.textColor = font_color
        text_style.alignment = {"left": 0, "center": 1, "right": 2}.get(align, 0)

        if font_weight == "bold":
            text_style.fontName = "Helvetica-Bold"

        # Create the paragraph object
        self.paragraph = Paragraph(self.text, text_style)

        # Get wrapped size
        return self.paragraph.wrap(availWidth, availHeight)

    def draw(self):
        """Draws the text inside the PDF."""
        if self.paragraph:
            self.paragraph.drawOn(self.canv, 0, 0)
