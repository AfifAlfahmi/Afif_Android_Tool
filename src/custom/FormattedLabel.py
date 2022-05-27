from kivy.clock import Clock
from kivy.core.text import Label
from kivy.graphics import Color, Rectangle
from kivy.properties import ListProperty


class FormattedLabel(Label):
    background_color = ListProperty()

    def __init__(self, *args, **kwargs):
        Label.__init__(self, *args, **kwargs)
        Clock.schedule_once(lambda dt: self.initialize_widget(), 0.002)

    def initialize_widget(self):
        self.canvas.before.add(Color(self.background_color))
        self.canvas.before.add(Rectangle(pos=self.pos, size=self.size))
        self.text_size = self.size
        self.halign = 'left'
        self.valign = 'top'
        self.bold = True