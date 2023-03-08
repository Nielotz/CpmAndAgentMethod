from kivy.uix.widget import Widget
from kivy.graphics import Line, Ellipse, Color, Point
from kivy.uix.button import Button
from kivy.uix.label import Label

#To Do
#Zapewnić by na siebie nie nachodziły

class ActionWidget(Widget):
    pass

class EventWidget(Widget):
    radius = 60
    pos = (20, 40)
    number = 2
    
    
    def __init__(self, **kwargs):
        super(EventWidget, self).__init__(**kwargs)

        
        
        with self.canvas:
            Ellipse(pos=self.pos, size=(self.radius, self.radius))
            Ellipse(pos=self.pos, size=(5,5), color=(1,0,0))
        label = Label(text=str(self.number) , color=(1,0,1), outline_color=(0,1,0))
        print(label.size)
        print(label.width)
        print(label.height)
        center_of_circle = (self.radius/2, self.radius/2)
        pos_of_number = (center_of_circle[0], center_of_circle[1])
        label.pos = self.pos
        self.add_widget(label)



class GraphWidget(Widget):
    def __init__(self, **kwargs):
        super(GraphWidget, self).__init__(**kwargs)
        self.add_widget(Button(text="test"))
        self.add_widget(EventWidget(pos=(500,50)))
        self.add_widget(EventWidget())
        # with self.canvas:
        #     Line(points=(1,5,23,43,44,55))
        #     Ellipse(pos=(self.width/2, self.height/2), size=(30,30))