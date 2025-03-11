from reportlab.platypus import Flowable

class Component(Flowable):
    """Base class for all components in the FlexPDF library."""

    def __init__(self, style=None):
        """
        :param style: Dictionary of styles (e.g., {'text_color': 'black', 'font_size': 12})
        """
        super().__init__()
        self.style = style or {}  # Default to empty style dictionary

    def apply_style(self, canvas):
        """Apply styles like text color, font size, etc."""
        if 'text_color' in self.style:
            canvas.setFillColor(self.style['text_color'])
        if 'font_size' in self.style:
            canvas.setFont("Helvetica", self.style['font_size'])

    def wrap(self, availWidth, availHeight):
        """Default wrap method, should be overridden by child components."""
        return availWidth, 0  # Components must define their own height

    def draw(self):
        """Default draw method, must be overridden."""
        raise NotImplementedError("Each component must implement draw()")
