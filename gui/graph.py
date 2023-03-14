from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.graphics import Line, Ellipse, Color, Callback, Rectangle
from kivy.uix.label import Label
from kivy.uix.effectwidget import FXAAEffect, EffectWidget, HorizontalBlurEffect
from math import sin, cos, atan , pi
from kivy.core.window import Window
import cpm.network as network
#To Do
# Zapewnić by na siebie nie nachodziły
# Dodać pozorną akcje
# Dodać ścieżke krytyczną

class InfoWitdget(Widget):
    visible:float = 0.

    def __init__(self, number: str = "233", earliest_time:int = 0, latest_time:int = 0, reserve_time:int = 0,pos:tuple[int,int]=(10,10),  **kwargs):
        super(InfoWitdget, self).__init__(**kwargs)
        self.pos = pos
        self.number = number
        with self.canvas:
            Color(.5, .5, 0.5)
            Rectangle(pos=self.pos)

            # self.visible_callback = Callback(self.draw)
            
        
    # def draw(self, instr):
    #     with self.canvas:
    #         Color(.5, .5, self.visible/10, self.visible)
    #         print("visible "+self.number+": " + str(self.visible))
    #         Rectangle(pos=self.pos)

    # def show(self):
    #     self.visible = 1.
    #     self.visible_callback.ask_update()

    # def hide(self):
    #     self.visible = 0.
    #     self.visible_callback.ask_update()


class EventWidget(Widget):
    circle_color: tuple[float,float,float] = (0,1,1)
    line_color: tuple[float,float,float] = (0,1,0)
    text_color: tuple[float,float,float] = (1,0,1)
    diameter: int = 75
    pos: tuple[int, int] = (20, 40)
    number: str = 233
    offset: int = 25
    earliest_time:int = 222
    latest_time:int = 122
    reserve_time:int = 123
    info_widget_is_visible = False

    def __init__(self, number: str = "1", earliest_time:int = 0, latest_time:int = 0, reserve_time:int = 0,  **kwargs):
        super(EventWidget, self).__init__(**kwargs)
        self.number = number
        self.earliest_time = earliest_time
        self.latest_time = latest_time
        self.reserve_time = reserve_time

        self.radius = self.diameter / 2
        center_of_circle = (self.diameter / 2, self.diameter / 2)
        self.center_of_circle = (center_of_circle[0] + self.pos[0], center_of_circle[1] + self.pos[1])

        # Window.bind(mouse_pos=self.on_enter)

        with self.canvas:
            Color(self.circle_color[0],self.circle_color[1],self.circle_color[2])
            Ellipse(pos=self.pos, size=(self.diameter, self.diameter))
            Color(1, 0, 0)
            Line(points=(self.radius * cos(pi * 5 / 4) + self.center_of_circle[0], 
                         self.radius * sin(pi * 5 / 4) + self.center_of_circle[1],
                         self.radius * cos(pi / 4) + self.center_of_circle[0], 
                         self.radius * sin(pi / 4) + self.center_of_circle[1]),
                         width=1)
            Line(points=(self.radius * cos(pi * 3 / 4) + self.center_of_circle[0], 
                         self.radius * sin(pi * 3 / 4) + self.center_of_circle[1],
                         self.radius * cos(pi * 7 / 4) + self.center_of_circle[0], 
                         self.radius * sin(pi * 7 / 4) + self.center_of_circle[1]),
                         width=1)

        label_of_number = Label(text=str(self.number), color = self.text_color)
        label_of_number.pos = (self.pos[0] - label_of_number.width / 2 + center_of_circle[0],
                               self.pos[1] - label_of_number.height / 2 + center_of_circle[1] + self.offset)
        self.add_widget(label_of_number)

        label_of_time_reserve = Label(text=str(self.reserve_time), color = self.text_color)
        label_of_time_reserve.pos = (self.pos[0] - label_of_time_reserve.width / 2 + center_of_circle[0],
                               self.pos[1] - label_of_time_reserve.height / 2 + center_of_circle[1] - self.offset)
        self.add_widget(label_of_time_reserve)

        label_of_earliest_time = Label(text=str(self.latest_time), color = self.text_color)
        label_of_earliest_time.pos = (self.pos[0] - label_of_number.width / 2 + center_of_circle[0] - self.offset,
                               self.pos[1] - label_of_number.height / 2 + center_of_circle[1])
        self.add_widget(label_of_earliest_time)

        label_of_latest_time = Label(text=str(self.earliest_time), color = self.text_color)
        label_of_latest_time.pos = (self.pos[0] - label_of_number.width / 2 + center_of_circle[0] + self.offset,
                               self.pos[1] - label_of_number.height / 2 + center_of_circle[1])
        self.add_widget(label_of_latest_time)

        self.info_widget = InfoWitdget(pos=self.pos, number=number)
        # self.add_widget(self.info_widget)

    def get_radius(self):
        return self.radius
    
    def get_center_of_circle(self):
        return self.center_of_circle
    
    # def on_enter(self, window, pos):
    #     if pos[0] > self.pos[0] and pos[0] < self.pos[0] + self.diameter:
    #         if pos[1] > self.pos[1] and pos[1] < self.pos[1] + self.diameter:
    #             print(self.number)
    #             # self.info_widget.show()
    #             if self.info_widget_is_visible == False:
    #                 self.add_widget(self.info_widget, index=0)
    #                 self.info_widget_is_visible = True
    #     else:
    #         if self.info_widget_is_visible == True:
    #             self.info_widget_is_visible = False
    #             # self.info_widget.hide()
    #             self.remove_widget(self.info_widget)
                

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
            p0 = self.event_widget_0.get_center_of_circle()
            p1 = self.event_widget_1.get_center_of_circle()
            alpha = atan((p1[1] - p0[1]) / (p1[0] - p0[0]))
            Line(points=(radius_event_widget_0*cos(alpha)+p0[0],
                         radius_event_widget_0*sin(alpha)+p0[1],
                         -radius_event_widget_1*cos(alpha)+p1[0],
                         -radius_event_widget_1*sin(alpha)+p1[1]),
                 width=2)


class GraphHelpWidget(Widget):
    bacground_color = (.1, .1, .1, 0.9)
    pos_of_help_circle = (300,200)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        with self.canvas:
            Color(*self.bacground_color)
            Rectangle(size=(700., 500.), pos=(10,60))

        self.help_event_widget = EventWidget(pos=self.pos_of_help_circle)
        

        offset = self.help_event_widget.radius
        
        number_label = Label(text="numer zdarzenia")
        number_label.pos = (self.help_event_widget.center_of_circle[0] - number_label.width / 2,
                            self.help_event_widget.center_of_circle[1] + offset)
        
        earliest_time_label = Label(text="najpóźniejszy możliwy\nmoment zaistnienia zdarzenia")
        earliest_time_label.pos = (self.help_event_widget.center_of_circle[0] + offset + earliest_time_label.width,
                                   self.help_event_widget.center_of_circle[1] - earliest_time_label.height / 2)


        latest_time_label = Label(text="zapas (luz) czasu")
        latest_time_label.pos = (self.help_event_widget.center_of_circle[0] - latest_time_label.width / 2,
                                 self.help_event_widget.center_of_circle[1] - offset - latest_time_label.height)

        reserve_time_label = Label(text="najwcześniejszy możliwy\nmoment zaistnienia zdarzenia")
        reserve_time_label.pos = (self.help_event_widget.center_of_circle[0] - offset - reserve_time_label.width *2 ,
                                   self.help_event_widget.center_of_circle[1] - reserve_time_label.height / 2)


        self.add_widget(self.help_event_widget)
        self.add_widget(number_label)
        self.add_widget(earliest_time_label)
        self.add_widget(latest_time_label)
        self.add_widget(reserve_time_label)

        self.canvas.add(Ellipse(pos=self.help_event_widget.center_of_circle, size=(10,10)))



class GraphWidget(EffectWidget):
    is_help_page_enabled = False

    def __init__(self, **kwargs):
        super(GraphWidget, self).__init__(**kwargs)
        #self.effects = [FXAAEffect()]
        self.help_page = GraphHelpWidget()

    def set_network(self, network:network.Network):
        for node in network.nodes:
            print(node.duration)
            print(node.id_)
    
    def draw_graph(self, network:network.Network):
        prev_event_widgets_number:dict(str, int) = dict()
        next_event_widgets_number:dict(str, int) = dict()
        event_widgets = dict()
        action_widgets:dict(str, ActionWidget) = dict()

        for node in network.nodes_by_id.values():
            ids = node.id_.split("-")
            if ids[1] in prev_event_widgets_number:
                prev_event_widgets_number[ids[1]] += 1
            else:
                prev_event_widgets_number[ids[1]] = 1
            if ids[0] in next_event_widgets_number:
                next_event_widgets_number[ids[0]] += 1
            else:
                next_event_widgets_number[ids[0]] = 1


        for node in network.nodes_by_id.values():
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


        for node in network.nodes_by_id.values():
            ids = node.id_.split("-")
            action_widgets[node.id_] = ActionWidget() 
            action_widgets[node.id_].set_event_widget_0(event_widgets[ids[0]])
            action_widgets[node.id_].set_event_widget_1(event_widgets[ids[1]])
          

        for key in action_widgets:
            self.add_widget(action_widgets[key],index=1000)


        # self.add_widget(Button(text="Pomoc", pos=(10,10),size_hint = (.05,.05)))
        help_button = Button(text="Pomoc",size = (70,40), pos=(10,10),size_hint = (None,None));
        help_button.bind(on_press = self.help_button_callback)
        self.add_widget(help_button)
    
    def help_button_callback(self, event):
        if self.is_help_page_enabled == True:
            self.is_help_page_enabled = False
            self.remove_widget(self.help_page)
        else:
            self.is_help_page_enabled = True
            self.add_widget(self.help_page)

        print("pressed")
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