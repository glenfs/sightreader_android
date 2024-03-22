from kivy.graphics import Rectangle, Color
from kivy.uix.label import Label


class StyledLabel(Label):
    def __init__(self, **kwargs):
        super(StyledLabel, self).__init__(**kwargs)
        self.rect = None
        self.font_size = '24sp'
        self.color = (1, 1, 1, 1)  # White text color

        # Set the background color and border
        with self.canvas.before:
            Color(0.2, 0.6, 1, 1)  # Set background color (RGBA)
            self.rect = Rectangle(pos=self.pos, size=self.size)

    def on_size(self, *args):
        self.rect.size = self.size

    def on_pos(self, *args):
        self.rect.pos = self.pos
