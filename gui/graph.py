from kivy.uix.widget import Widget
from kivy.graphics import Line, Ellipse, Color, Callback
from kivy.uix.label import Label
from kivy.uix.effectwidget import FXAAEffect, EffectWidget, HorizontalBlurEffect
from math import sin, cos, atan , pi
import cpm.network as network
#To Do
#Zapewnić by na siebie nie nachodziły



class EventWidget(Widget):
    circle_color: tuple[float,float,float] = (0,1,1)
    line_color: tuple[float,float,float] = (0,1,0)
    diameter: int = 70
    pos: tuple[int, int] = (20, 40)
    number: str = 233
    offset: int = 25
    earliest_time:int = 222
    latest_time:int = 122
    reserve_time:int = 123

    def __init__(self, number: str = "233", earliest_time:int = 0, latest_time:int = 0, reserve_time:int = 0,  **kwargs):
        super(EventWidget, self).__init__(**kwargs)
        self.number = number
        self.earliest_time = earliest_time
        self.latest_time = latest_time
        self.reserve_time = reserve_time

        self.radius = self.diameter/2
        center_of_circle = (self.diameter/2, self.diameter/2)
        self.pos_center_of_circle = (center_of_circle[0] + self.pos[0], center_of_circle[1] + self.pos[1])

        with self.canvas:
            Color(self.circle_color[0],self.circle_color[1],self.circle_color[2])
            Ellipse(pos=self.pos, size=(self.diameter, self.diameter))
            Color(1,0,0)
            Line(points=(self.radius * cos(pi * 5 / 4) + self.pos_center_of_circle[0], 
                         self.radius * sin(pi * 5 / 4) + self.pos_center_of_circle[1],
                         self.radius * cos(pi / 4) + self.pos_center_of_circle[0], 
                         self.radius * sin(pi / 4) + self.pos_center_of_circle[1]),
                         width=1)
            Line(points=(self.radius * cos(pi * 3 / 4) + self.pos_center_of_circle[0], 
                         self.radius * sin(pi * 3 / 4) + self.pos_center_of_circle[1],
                         self.radius * cos(pi * 7 / 4) + self.pos_center_of_circle[0], 
                         self.radius * sin(pi * 7 / 4) + self.pos_center_of_circle[1]),
                         width=1)

        label_of_number = Label(text=str(self.number), color=(1,0,1))
        label_of_number.pos = (self.pos[0] - label_of_number.width / 2 + center_of_circle[0],
                               self.pos[1] - label_of_number.height / 2 + center_of_circle[1] + self.offset)
        self.add_widget(label_of_number)

        label_of_time_reserve = Label(text=str(self.reserve_time), color = (1, 0, 1))
        label_of_time_reserve.pos = (self.pos[0] - label_of_time_reserve.width / 2 + center_of_circle[0],
                               self.pos[1] - label_of_time_reserve.height / 2 + center_of_circle[1] - self.offset)
        self.add_widget(label_of_time_reserve)

        label_of_earliest_time = Label(text=str(self.latest_time), color = (1, 0, 1))
        label_of_earliest_time.pos = (self.pos[0] - label_of_number.width / 2 + center_of_circle[0] - self.offset,
                               self.pos[1] - label_of_number.height / 2 + center_of_circle[1])
        self.add_widget(label_of_earliest_time)

        label_of_latest_time = Label(text=str(self.earliest_time), color = (1, 0, 1))
        label_of_latest_time.pos = (self.pos[0] - label_of_number.width / 2 + center_of_circle[0] + self.offset,
                               self.pos[1] - label_of_number.height / 2 + center_of_circle[1])
        self.add_widget(label_of_latest_time)

    def get_radius(self):
        return self.radius
    
    def get_pos_center_of_circle(self):
        return self.pos_center_of_circle


class ActionWidget(Widget):
    event_widget_0: EventWidget = EventWidget()
    event_widget_1: EventWidget = EventWidget()

    def __init__(self, **kwargs):
        super(ActionWidget, self).__init__( **kwargs)

        self.info_label = Label(text=str(), color=(1,0,0))

        with self.canvas:
            Color(0,1,1)
            self.cb = Callback(self.draw)

    def set_event_widget_0(self, event_widget: EventWidget):
        self.event_widget_0 = event_widget
        self.cb.ask_update()

    def set_event_widget_1(self, event_widget: EventWidget):
        self.event_widget_1 = event_widget
        self.cb.ask_update()

    def draw(self, instr):
        with self.canvas:
            radius_event_widget_0 = self.event_widget_0.get_radius() + 1
            radius_event_widget_1 = self.event_widget_1.get_radius() + 1
            p0 = self.event_widget_0.get_pos_center_of_circle()
            p1 = self.event_widget_1.get_pos_center_of_circle()
            alpha = atan((p1[1] - p0[1]) / (p1[0] - p0[0]))
            Line(points=(radius_event_widget_0*cos(alpha)+p0[0],
                         radius_event_widget_0*sin(alpha)+p0[1],
                         -radius_event_widget_1*cos(alpha)+p1[0],
                         -radius_event_widget_1*sin(alpha)+p1[1]),
                 width=2)



class GraphWidget(EffectWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.effects = [FXAAEffect()]

        # e0:EventWidget = EventWidget(pos=(10,300))
        # e1:EventWidget = EventWidget(pos=(150,100))
        # e2:EventWidget = EventWidget(pos=(500,200))
        # e3:EventWidget = EventWidget(pos=(500,350))
        # self.add_widget(e0)
        # self.add_widget(e1)
        # self.add_widget(e2)
        # self.add_widget(e3)

        # a0:ActionWidget = ActionWidget()
        # a0.set_event_widget_0(e0)
        # a0.set_event_widget_1(e1)
        # self.add_widget(a0)
        # a1:ActionWidget = ActionWidget()
        # a1.set_event_widget_0(e1)
        # a1.set_event_widget_1(e2)
        # self.add_widget(a1)
        # a2:ActionWidget = ActionWidget()
        # a2.set_event_widget_0(e1)
        # a2.set_event_widget_1(e3)
        # self.add_widget(a2)
        

    def set_network(self, network:network.Network):
        for node in network.nodes:
            print(node.duration)
            print(node.id_)
    
    def draw_graph(self, network:network.Network):
        prev_event_widgets_number:dict(str, int) = dict()
        next_event_widgets_number:dict(str, int) = dict()
        event_widgets = dict()
        action_widgets:dict(str, ActionWidget) = dict()

        for node in network.nodes:
            ids = node.id_.split("-")
            if ids[1] in prev_event_widgets_number:
                prev_event_widgets_number[ids[1]] += 1
            else:
                prev_event_widgets_number[ids[1]] = 1
            if ids[0] in next_event_widgets_number:
                next_event_widgets_number[ids[0]] += 1
            else:
                next_event_widgets_number[ids[0]] = 1


        for node in network.nodes:
            

            ids = node.id_.split("-")
            if not ids[0] in event_widgets:
                event_widgets[ids[0]] = EventWidget(pos=(150 * int(ids[0]) - 150, 300), 
                                                    number=ids[0], 
                                                    earliest_time = node.early_start,
                                                    latest_time = node.late_start,
                                                    reserve_time = node.possible_delay)
            if not ids[1] in event_widgets:
                event_widgets[ids[1]] = EventWidget(pos=(150 * int(ids[1]) - 150, 300), number=ids[1])

            if next_event_widgets_number[ids[0]] > 1:
                event_widgets[ids[1]] = EventWidget(pos=(150 * int(ids[1]) - 150 , # * next_event_widgets_number[ids[0]]
                                                         300 + 150*(next_event_widgets_number[ids[0]] - 1)), 
                                                    number=ids[1])
                next_event_widgets_number[ids[0]] -= 1


        for key in event_widgets:       
            self.add_widget(event_widgets[key])


        for node in network.nodes:
            ids = node.id_.split("-")
            action_widgets[node.id_] = ActionWidget() 
            action_widgets[node.id_].set_event_widget_0(event_widgets[ids[0]])
            action_widgets[node.id_].set_event_widget_1(event_widgets[ids[1]])
          

        for key in action_widgets:
            self.add_widget(action_widgets[key])

        # iteration:int = 0
        # for node in network.nodes:
        #     event_widgets[node.id_] = EventWidget(pos=(150 * iteration, 300), number=node.id_)
        #     self.add_widget(event_widgets[node.id_])
        #     iteration += 1
            
        # for node in network.nodes:
        #     for prev in node.prev_nodes:
        #         if prev == '':
        #             break

        #         action_widget = ActionWidget()   
        #         action_widget.set_event_widget_0(event_widgets[prev])
        #         action_widget.set_event_widget_1(event_widgets[node.id_])
        #         self.add_widget(action_widget)   
            # print(iteration)

        # with self.canvas:
        #     Line(points=(1,5,23,43,44,55))
        #     Ellipse(pos=(self.width/2, self.height/2), size=(30,30))