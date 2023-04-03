from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.graphics import Line, Ellipse, Color, Callback, Rectangle
from kivy.uix.label import Label
from kivy.uix.effectwidget import FXAAEffect, EffectWidget, HorizontalBlurEffect
from math import sin, cos, atan , pi, sqrt
from kivy.core.window import Window
import cpm.network as network


class InfoWitdget(Widget):
    visible:float = 0.

    def __init__(self, name: str = "233", earliest_time:int = 0, latest_time:int = 0, reserve_time:int = 0,pos:tuple[int,int]=(10,10),  **kwargs):
        super(InfoWitdget, self).__init__(**kwargs)
        self.pos = pos
        self.name = name
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
    name: str = "233"
    offset: int = 25
    earliest_time:int = 222
    latest_time:int = 122
    reserve_time:int = 123
    # info_widget_is_visible = False

    def __init__(self, name: str = "1", earliest_time:int = 0, latest_time:int = 0, reserve_time:int = 0,  **kwargs):
        super(EventWidget, self).__init__(**kwargs)
        self.name = name
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

        label_of_number = Label(text=str(self.name), color = self.text_color)
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

        self.info_widget = InfoWitdget(pos=self.pos, name=name)
        # self.add_widget(self.info_widget)

    def get_radius(self):
        return self.radius
    
    def get_center_of_circle(self):
        return self.center_of_circle
     

class ActionWidget(Widget):
    event_widget_0: EventWidget = EventWidget()
    event_widget_1: EventWidget = EventWidget()
    info_label = Label(text=str("eee"))
    middle =(0,0)
    dashed_lines = 4
    color = (0., 1., 1., 1.)
    critical_color = (0.5, 0., 0., 1.)
    label_background_color = (0., 1., 1., 1.)
    label_text_color = (1.,0.,0., 1.)

    def __init__(self, 
                 action_name:str = "",
                 action_time:float = 0,
                 is_real:bool = True,
                 is_critical:bool = True,
                 event_widget_0:EventWidget = EventWidget(), 
                 event_widget_1:EventWidget = EventWidget(), 
                 **kwargs):
        super(ActionWidget, self).__init__( **kwargs)
        
        if is_critical:
            self.color = self.critical_color
            self.label_background_color = self.critical_color

        self.event_widget_0 = event_widget_0
        self.event_widget_1 = event_widget_1
        self.info_label_text = action_name + " " + str(action_time)

        with self.canvas:
            Color(self.color[0], self.color[1], self.color[2], self.color[3])
            radius_event_widget_0 = self.event_widget_0.get_radius() + 1
            radius_event_widget_1 = self.event_widget_1.get_radius() + 1
            p0 = self.event_widget_0.get_center_of_circle()
            p1 = self.event_widget_1.get_center_of_circle()
            try:
                alpha = atan((p1[1] - p0[1]) / (p1[0] - p0[0]))
                points = (radius_event_widget_0 * cos(alpha) + p0[0],
                          radius_event_widget_0 * sin(alpha) + p0[1],
                          -radius_event_widget_1 * cos(alpha) + p1[0],
                          -radius_event_widget_1 * sin(alpha) + p1[1]
                          )
                
            
                norm_point = (points[2] - points[0],
                            points[3] - points[1])
                
                fi = atan(norm_point[1] / norm_point[0])
            except:
                alpha = 0
                if p0[1] > p1[1]:
                    points = (p0[0],
                              p0[1] - radius_event_widget_0,
                              p1[0],
                              p1[1] + radius_event_widget_1)
                    fi = pi * 3 / 2
                else:
                    points = (p0[0],
                              p0[1] + radius_event_widget_0,
                              p1[0],
                              p1[1] - radius_event_widget_1)
                    fi = pi / 2
                alpha = fi

            self.middle = ((points[0] + points[2]) / 2,
                           (points[1] + points[3]) / 2)

            norm_point = (points[2] - points[0],
                          points[3] - points[1])
            
            radius = (sqrt(norm_point[0] * norm_point[0] + norm_point[1] * norm_point[1]))

            if is_real: 
                Line(points=points,
                     width=2)
            else:      
                radius_change = radius / (self.dashed_lines * 2) - 1
                
                sth_radius = radius
                while sth_radius > 0:
                    sth_point = (sth_radius * cos(fi) + points[0],
                                 sth_radius * sin(fi) + points[1],
                                 (sth_radius - radius_change) * cos(fi) + points[0],
                                 (sth_radius - radius_change) * sin(fi) + points[1])
                    Line(points=sth_point,
                         width=2)
                    sth_radius -= radius_change * 2
            
            
            #Draw Arrow
            arrowhead_legth:float = 20
            arrowhead_angle:float = pi / 6
            arrow_vec = (arrowhead_legth,
                         0,
                         arrowhead_legth,
                         0)
            
            arrow_vec = (arrow_vec[0] * cos(pi + arrowhead_angle + alpha) - arrow_vec[1] * sin(pi + arrowhead_angle + alpha),
                         arrow_vec[0] * sin(pi + arrowhead_angle + alpha) + arrow_vec[1] * cos(pi + arrowhead_angle + alpha),
                         arrow_vec[2] * cos(pi - arrowhead_angle + alpha) - arrow_vec[3] * sin(pi - arrowhead_angle + alpha),
                         arrow_vec[2] * sin(pi - arrowhead_angle + alpha) + arrow_vec[3] * cos(pi - arrowhead_angle + alpha))
            
            arrow_vec = (arrow_vec[0]+ points[2],
                         arrow_vec[1]+ points[3],
                         arrow_vec[2]+ points[2],
                         arrow_vec[3]+ points[3])

            arrow_points = (points[2],
                            points[3],
                            arrow_vec[0],
                            arrow_vec[1],
                            points[2],
                            points[3],
                            arrow_vec[2],
                            arrow_vec[3])
            Line(points=arrow_points,
                     width=1.5)
        
        label_size = 50
        if len(self.info_label_text) > 8:
            label_size = int(len(self.info_label_text) * 50 / 8)
        self.info_label = Label(text=self.info_label_text,
                                size=(label_size, 20), 
                                color=(self.label_text_color[0],
                                       self.label_text_color[1],
                                       self.label_text_color[2]), 
                                font_size=12)
        
        self.info_label.pos = (self.middle[0] - self.info_label.size[0] / 2,
                               self.middle[1] - self.info_label.size[1] / 2)
        with self.info_label.canvas.before:
            Color(self.label_background_color[0],
                  self.label_background_color[1],
                  self.label_background_color[2],
                  self.label_background_color[3])
            Rectangle(pos=self.info_label.pos, size=self.info_label.size)
        self.add_widget(self.info_label)

        
class GraphHelpWidget(Widget):
    bacground_color = (.1, .1, .1, 0.9)
    pos_of_bottom_help = (300,150)
    pos_of_upper_help = (50,320)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        with self.canvas:
            Color(*self.bacground_color)
            Rectangle(size=(700., 500.), pos=(10,60))

#Draw upper of help page
        self.upper_event_widget_0 = EventWidget(pos = self.pos_of_upper_help)
        self.upper_event_widget_1 = EventWidget(pos = (self.pos_of_upper_help[0] + 500, self.pos_of_upper_help[1]))
        self.upper_action_widget = ActionWidget(action_name="A", 
                                                action_time=5,
                                                event_widget_0=self.upper_event_widget_0,
                                                event_widget_1=self.upper_event_widget_1)
        
        self.add_widget(self.upper_event_widget_0)
        self.add_widget(self.upper_event_widget_1)
        self.add_widget(self.upper_action_widget)

        offset = self.upper_event_widget_0.radius + 15
        event_widget_0_label = Label(text="Zdarzenie 1", size_hint=(None, None))
        event_widget_0_label.size = (130,50)
        event_widget_0_label.pos = (self.upper_event_widget_0.center_of_circle[0] - event_widget_0_label.width / 2,
                            self.upper_event_widget_0.center_of_circle[1] + offset)
        event_widget_1_label = Label(text="Zdarzenie 2", size_hint=(None, None))
        event_widget_1_label.size = (130,50)
        event_widget_1_label.pos = (self.upper_event_widget_1.center_of_circle[0] - event_widget_1_label.width / 2,
                            self.upper_event_widget_1.center_of_circle[1] + offset)

        action_widget_label = Label(text="        Czynność:\nnazwa : czas trwania", size_hint=(None, None))
        action_widget_label.size = (130,50)
        action_widget_label.pos = ((self.upper_event_widget_0.center_of_circle[0] + self.upper_event_widget_1.center_of_circle[0]) / 2 - action_widget_label.width / 2,
                                   self.upper_event_widget_1.center_of_circle[1] + 20)

        self.add_widget(event_widget_0_label)
        self.add_widget(event_widget_1_label)
        self.add_widget(action_widget_label)

        # self.canvas.add(Ellipse(pos=action_widget_label.pos, size=(10,10)))

#Draw bottom of help page
        self.help_event_widget = EventWidget(pos=self.pos_of_bottom_help)
        offset = self.help_event_widget.radius + 15
        
        number_label = Label(text="numer zdarzenia", size_hint=(None, None))
        number_label.size = (130,50)
        number_label.pos = (self.help_event_widget.center_of_circle[0] - number_label.width / 2,
                            self.help_event_widget.center_of_circle[1] + offset)
        
        with number_label.canvas:
            Color(0, 1, 0, 0.25)
            Rectangle(pos=number_label.pos, size=number_label.size)

        earliest_time_label = Label(text="najpóźniejszy możliwy\nmoment zaistnienia zdarzenia")
        earliest_time_label.size = (220,50)
        earliest_time_label.pos = (self.help_event_widget.center_of_circle[0] + offset ,
                                   self.help_event_widget.center_of_circle[1] - earliest_time_label.height / 2)
        with earliest_time_label.canvas:
            Color(0, 1, 0, 0.25)
            Rectangle(pos=earliest_time_label.pos, size=earliest_time_label.size)

        latest_time_label = Label(text="zapas (luz) czasu")
        latest_time_label.size = (130,50)
        latest_time_label.pos = (self.help_event_widget.center_of_circle[0] - latest_time_label.width / 2,
                                 self.help_event_widget.center_of_circle[1] - offset - latest_time_label.height)
        with latest_time_label.canvas:
            Color(0, 1, 0, 0.25)
            Rectangle(pos=latest_time_label.pos, size=latest_time_label.size)

        reserve_time_label = Label(text="najwcześniejszy możliwy\nmoment zaistnienia zdarzenia")
        reserve_time_label.size = (220,50)
        reserve_time_label.pos = (self.help_event_widget.center_of_circle[0] - offset - reserve_time_label.width ,
                                   self.help_event_widget.center_of_circle[1] - reserve_time_label.height / 2)
        with earliest_time_label.canvas:
            Color(0, 1, 0, 0.25)
            Rectangle(pos=reserve_time_label.pos, size=reserve_time_label.size)


        self.add_widget(self.help_event_widget)
        self.add_widget(number_label)
        self.add_widget(earliest_time_label)
        self.add_widget(latest_time_label)
        self.add_widget(reserve_time_label)


class GraphWidget(EffectWidget):
    is_move_enabled = False 
    x_distance = 200
    y_distance = 150

    def __init__(self, network:network.Network, **kwargs):
        super(GraphWidget, self).__init__(**kwargs)
        self.network = network
        #self.effects = [FXAAEffect()]
        
        self.old_touch_pos = [0,0]
        self.draw_graph(self.network)
    
    def draw_graph(self, network:network.Network.Graph):
        event_widgets = dict()
        action_widgets = dict()

        network.head.node.event

        x_pos = 0
        y_pos = self.y_distance
        
        def is_on_critical_path(node_id:str, critical_paths:list)->bool:
            for path in critical_paths:
                for path_node_id in path:
                    if path_node_id == node_id:
                        return True
            return False
        
        def draw_node(node:network.GraphNode, x_pos, y_pos):
            if node.id_ == 'FINISH' or not node.id_.find('apparent_'):
                return
            for tmp in node.next_graph_nodes:
                draw_node(tmp, x_pos + self.x_distance, y_pos)
                y_pos += self.y_distance
            
            event_widgets[node.id_] = EventWidget(name=node.id_,
                                                  pos=(x_pos, y_pos - self.y_distance),
                                                  earliest_time=node.node.event.early_final,
                                                  latest_time=node.node.event.late_final,
                                                  reserve_time=node.node.event.possible_delay)
        draw_node(network.head,x_pos,y_pos)

        # Genereate arrows
        for activity_key in network.graph_node_by_activity_id:
            activity:network.GraphNode = network.graph_node_by_activity_id[activity_key]
            prev_nodes = activity.prev_graph_nodes
            for node in prev_nodes:
                if not str(node.id_).find("apparent_"):
                    action_widgets[node.id_] = ActionWidget(action_name=node.id_,
                                                            event_widget_0=event_widgets[node.prev_graph_nodes[0].id_],
                                                            event_widget_1=event_widgets[activity.id_],
                                                            action_time=activity.node.activity.duration,
                                                            is_real=False,
                                                            is_critical=is_on_critical_path(activity.id_, network.critical_paths)
                                                            )
                    continue
                if not activity.id_ in action_widgets and str(node.id_).find("apparent_") and activity.id_ in event_widgets:
                    action_widgets[activity.id_] = ActionWidget(action_name=activity.id_,
                                                            event_widget_0=event_widgets[node.id_],
                                                            event_widget_1=event_widgets[activity.id_],
                                                            action_time=activity.node.activity.duration,
                                                            is_critical=is_on_critical_path(activity.id_, network.critical_paths)
                                                            )

        for node in event_widgets:
            self.add_widget(event_widgets[node])    

        for action in action_widgets:
            self.add_widget(action_widgets[action])
      
    def on_touch_move(self, touch):
        modifier = 0.7
        if self.is_move_enabled:
            self.pos = [self.pos[0] + int((touch.x - self.old_touch_pos[0]) * modifier), 
                        self.pos[1] + int((touch.y - self.old_touch_pos[1]) * modifier)]
            # print("mouse old", self.old_touch_pos)
            # print("mouse new", touch)
            print("pos", self.pos)
            self.old_touch_pos = touch.pos

        return super().on_touch_move(touch)
    
    def on_touch_down(self, touch):
        self.old_touch_pos = touch.pos
        print("mouse down", touch)

        return super().on_touch_down(touch)
    

class GraphMeneger(EffectWidget):
    is_help_page_enabled = False
    is_move_enabled = False 

    def __init__(self, net,  **kwargs):
        super(GraphMeneger, self).__init__(**kwargs)
#  
        self.help_page = GraphHelpWidget()

        self.graph_widget = GraphWidget(network=net, pos=(0,0)) #size=(100,100), size_hint=(None, None), pos=(300,100)
        self.add_widget(self.graph_widget)

        '''------------- HELP BUTTON ------------'''
        help_button = Button(text="Pomoc",size = (70,40), pos=(10,10),size_hint = (None,None))
        help_button.bind(on_press = self.help_button_callback) # type: ignore
        self.add_widget(help_button)

        '''------------- MOVE BUTTON ------------'''
        move_button = Button(text="Move", size = (70,40), pos=(85,10), size_hint = (None,None))
        move_button.bind(on_press = self.move_button_callback) # type: ignore
        self.add_widget(move_button)

        # Pirnt net
        for node in net.graph_node_by_activity_id:
            print(node)
            print(net.graph_node_by_activity_id[node])

    def help_button_callback(self, event):
        if self.is_help_page_enabled == True:
            self.is_help_page_enabled = False
            self.remove_widget(self.help_page)
        else:
            self.is_help_page_enabled = True
            self.add_widget(self.help_page)


    def move_button_callback(self, event):
        if self.is_move_enabled:
        # self.graph_widget.is_move_enabled = not self.graph_widget.is_move_enabled
            self.is_move_enabled = False
        else:
            self.is_move_enabled = True
        self.graph_widget.is_move_enabled = self.is_move_enabled