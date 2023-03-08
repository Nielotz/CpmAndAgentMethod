from kivy.uix.widget import Widget
from kivy.graphics import Line, Ellipse, Color
from kivy.uix.button import Button

class EventWidget(Widget):
    pass

class GraphWidget(Widget):
    def __init__(self, **kwargs):
        super(GraphWidget, self).__init__(**kwargs)
        self.add_widget(Button(text="test"))
        with self.canvas:
            Line(points=(1,5,23,43,44,55))
            Ellipse(pos=(self.width/2, self.height/2), size=(30,30))