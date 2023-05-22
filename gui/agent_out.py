from math import sin, cos, atan, pi, sqrt

from kivy.graphics import Line, Ellipse, Color, Rectangle
from kivy.uix.button import Button
from kivy.uix.effectwidget import EffectWidget
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, NoTransition, Screen
from agent.agent import AgentData
from agent.supply_chain import FictionalTrader

# To do
# -> move labels
# -> better colors

# class AgentData:
#     cost: float = 1111
#     income: float = 2222
#     profit: float = 223
#     profit_table: list[list[int]] = [[1,2,3],[4,5,6]]
#     optimal_transport_table: list[list[int]] = [[153,7,8],[9,0,1]]


# class AgentData:
#     total_products_cost: float = 5552
#     total_transport_cost: float = 255
#     total_cost: float = 1111
#     total_income: float = 2222
#     total_profit: float = 223
#     # buyers: [str]  # Headers in tables.
#     # sellers: [str]  # Headers in tables.
#     profit_table: list[list[float, ]] = [[1,2,3],[1,2,3],[4,5,6]]
#     optimal_transport_table: list[list[float, ]] = [[153,7,8],[1,2,3],[9,0,1]]

class ColorLabel(Label):
    def __init__(self, bacground_color=(1., 0., 1., 0.25), **kwargs):
        super().__init__(**kwargs)
        self.bacground_color = bacground_color
        self.gap = 2

    def on_size(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*self.bacground_color)
            Rectangle(pos=(self.pos[0]+self.gap, self.pos[1]+self.gap), 
                      size=(self.size[0]-2*self.gap, self.size[1]-2*self.gap))


class AgentWidget(Widget):
    def __init__(self, agent_data: AgentData, **kwargs):
        super().__init__(**kwargs)
        self.agent_data = agent_data
        if isinstance(self.agent_data.buyers[len(self.agent_data.buyers) - 1], FictionalTrader):
            self.fictional = True
        else:
            self.fictional = False

        self.draw_summary()
        self.draw_profit_table()
        self.draw_optimal_transport_table()
       

        
    def draw_summary(self):
        summary_size = (320, 80)
        summary_pos = ((Window.size[0] - summary_size[0]) / 2, Window.size[1] - 2 * summary_size[1]+50)
        summary_padding = 5
        label_size = (100,20)
        text_color = (.1, .1, .1)
        font_size = 18
        

        with self.canvas:
            Color(.6, .6, .6, 0.3)
            Rectangle(size=summary_size, pos=summary_pos)
        

        text='[b]Income: [color=#008000]' + str(self.agent_data.total_income) + '[/color][/b]'
        income_label = Label(text=text, 
                             color=text_color,
                             size=label_size, 
                             halign='left',
                             size_hint=(None, None),
                             font_size=font_size,
                             markup=True)
        income_label.pos = (summary_padding, summary_size[1] - summary_padding - label_size[1])
        income_label.bind(texture_size=income_label.setter('size'))


        text='[b]Cost: [color=#800000]' + str(self.agent_data.total_cost) + '[/color][/b]'
        cost_label = Label(text=text, 
                             color=text_color,
                             size=label_size, 
                             halign='left',
                             size_hint=(None, None),
                             font_size=font_size,
                             markup=True)
        cost_label.pos = (summary_padding, summary_size[1] - summary_padding - 2* label_size[1])
        cost_label.bind(texture_size=cost_label.setter('size'))

        
        text='[b]Profit: [color=#00C000]'+str(self.agent_data.total_profit) + '[/color][/b]'
        profit_label = Label(text=text, 
                             color=text_color,
                             size=label_size, 
                             halign='left',
                            #  valign='center',
                             size_hint=(None, None),
                             font_size=font_size,
                             markup=True)
        profit_label.size = (profit_label.size[0], summary_size[1])
        profit_label.text_size = profit_label.size
        # profit_label.pos = (summary_size[0] - profit_label.size[0]-summary_padding, 0)
        profit_label.pos = (summary_padding, summary_padding)

        text='[b]Transport cost: [color=#700000]'+str(self.agent_data.total_transport_cost) + '[/color][/b]'
        transport_cost_label = Label(text=text, 
                             color=text_color,
                             size=label_size, 
                             halign='right',
                            #  valign='center',
                             size_hint=(None, None),
                             font_size=font_size,
                             markup=True)
        transport_cost_label.bind(texture_size=transport_cost_label.setter('size'))
        transport_cost_label.size = (transport_cost_label.size[0] + 100, label_size[1])
        transport_cost_label.text_size = transport_cost_label.size
        transport_cost_label.pos = (summary_size[0] - transport_cost_label.size[0] - summary_padding, 
                                    summary_size[1] / 2 + 5)

        text='[b]Products cost: [color=#700000]'+str(self.agent_data.total_products_cost) + '[/color][/b]'
        products_cost_label = Label(text=text, 
                             color=text_color,
                             size=label_size, 
                             halign='right',
                            #  valign='center',
                             size_hint=(None, None),
                             font_size=font_size,
                             markup=True)
        products_cost_label.bind(texture_size=products_cost_label.setter('size'))
        products_cost_label.size = (products_cost_label.size[0] + 100, label_size[1])
        products_cost_label.text_size = products_cost_label.size
        products_cost_label.pos = (summary_size[0] - products_cost_label.size[0] - summary_padding, 
                                   summary_size[1] / 2 - products_cost_label.size[1]+ 5)

        layout = RelativeLayout(pos=summary_pos)
        layout.add_widget(cost_label)
        layout.add_widget(income_label)
        layout.add_widget(profit_label)
        layout.add_widget(transport_cost_label)
        layout.add_widget(products_cost_label)

        self.add_widget(layout)

    def draw_optimal_transport_table(self):
        pos = (425, 100)
        size = (350, 300)
        
        with self.canvas:
            Color(0.3, 0.3, 0.3, 1.)
            Rectangle(size=size, pos=pos)

        layout = AnchorLayout(size=(size[0], 40), pos=(pos[0], pos[1] + size[1]))
        layout.add_widget(ColorLabel(text="Optimal transport table", 
                                                   bacground_color=(0.3, 0.3, 0.3,1.), 
                                                   color=(1, 1, .55),
                                                   font_size=18))
        
        self.add_widget(layout)
        self.add_widget(self.generate_table(pos,size,self.agent_data.optimal_transport_table))

    def draw_profit_table(self):
        pos = (25, 100)
        size = (350, 300)
        
        with self.canvas:
            Color(0.3, 0.3, 0.3, 1.)
            Rectangle(size=size, pos=pos)

        layout = AnchorLayout(size=(size[0], 40), pos=(pos[0], pos[1] + size[1]))
        layout.add_widget(ColorLabel(text="Profit table", 
                                                   bacground_color=(0.3, 0.3, 0.3,1.), 
                                                   color=(1, 1, .55),
                                                   font_size=18))
        
        # profit_table_label = Label(text="Profit table", color=(0,1,.55), size=(size[0],20), font_size=18)
        # profit_table_label.pos = (pos[0], pos[1] + size[1] - profit_table_label.size[1]-10)
        
        self.add_widget(layout)
        self.add_widget(self.generate_table(pos,size,self.agent_data.unit_profit_table))

    def generate_table(self, pos, size, data:list[list[int]]):
        background_color = (.9, .9, .9, 1.)
        text_color = (.25, .65, .25)
        font_size=15
        fictional=self.fictional

        layout = GridLayout(cols=len(data[0])+1, pos=pos, size=size)
        layout.add_widget(ColorLabel(text=" ", bacground_color=(0,0,0,0), font_size=font_size))
        tmp=""

        for i in range(len(data[0])):
            if fictional and i == len(data[0]) - 1:
                tmp = "F"
            else:
                tmp = str(i)
                
            layout.add_widget(ColorLabel(text="[b]R"+tmp+"[/b]",
                                         markup=True,
                                         color=text_color, 
                                         bacground_color=background_color,
                                         font_size=font_size))

        for i in range(len(data)):
            if fictional and i == len(data) - 1:
                tmp = "F"
            else:
                tmp = str(i)
            layout.add_widget(ColorLabel(text="[b]S"+tmp+"[/b]",
                                         markup=True, 
                                         color=text_color, 
                                         bacground_color=background_color,
                                         font_size=font_size))
            for j in data[i]:
                layout.add_widget(ColorLabel(text="[b]"+str(j)+"[/b]", 
                                             markup=True, 
                                             color=text_color, 
                                             bacground_color=background_color,
                                             font_size=font_size))

        return layout


class AgentManager(Widget):
    def __init__(self, datas, **kwargs):
        super().__init__(**kwargs)
        self.datas = datas
        self.data_id = 0

        self.agent_widget = AgentWidget(agent_data=self.datas[self.data_id], pos=(0,0))
        self.add_widget(self.agent_widget)

        self.next_data_button = Button(text="Next optimal solution",
                                          size=(200, 40),
                                          pos=(20, 10),
                                          size_hint=(None, None))
        self.next_data_button.bind(on_press=self.next_data_callback)
        self.add_widget(self.next_data_button)

    def next_data_callback(self, event):
        self.data_id += 1
        if self.data_id >= len(self.datas):
            self.data_id = 0

        self.remove_widget(self.agent_widget)
        self.agent_widget = AgentWidget(agent_data=self.datas[self.data_id], pos=(0,0))
        self.add_widget(self.agent_widget)

        
class TestAgentWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        datas = [AgentData(),AgentData()]
        self.add_widget(AgentManager(datas=datas))


