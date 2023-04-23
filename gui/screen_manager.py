from typing import Hashable, List, Dict

from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup

import data_input
import gui.graph as graph

from cpm.network.network import Network
from cpm.node import Node
from cpm.solver import Solver



class MyScreenManager(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.transition = NoTransition()
        self.add_widget(HomeScreen(name='home'))
        self.add_widget(TableScreen(name='table'))
        self.add_widget(CpmHomeScreen(name='cpmHome'))

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        button = Button(text='CPM method', size_hint=(.2, .1), pos_hint={'center_x': .5, 'center_y': .5})
        button.bind(on_press=self.go_to_cpm_home_Screen)
        self.add_widget(button)

        # add an information label to display messages
        info_label = Label(text='Logistic Simulator', size_hint=(1, None), pos_hint={'top': 1}, height=100, color=(0,0,0,1), font_size=30)
        self.add_widget(info_label)
        self.ids.info_label = info_label
    def go_to_cpm_home_Screen(self, instance):
        self.manager.current = 'cpmHome'
class CpmHomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # create a box layout for the screen
        box = BoxLayout(orientation='vertical', padding=10, spacing=10)
        input_data_button = Button(text='Input Data', size_hint=(.3, None), pos_hint={'left': 1, 'y': 0})
        read_data_button = Button(text='Input Data from file', size_hint=(.3, None), pos_hint={'left': 1, 'y': 0})
        input_data_button.bind(on_press=self.go_to_table_screen)

        # create a horizontal box layout for the buttons
        buttons_box = BoxLayout(orientation='horizontal', size_hint=(1, None), height=50, spacing=10)
        buttons_box.add_widget(input_data_button)
        buttons_box.add_widget(read_data_button)

        box.add_widget(buttons_box)
        self.add_widget(box)
        # add an information label to display messages
        info_label = Label(text='', size_hint=(1, None), height=50)
        self.add_widget(info_label)
        self.ids.info_label = info_label
    def go_to_table_screen(self, instance):
        self.manager.current = 'table'

class TableScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.table_data = []

        # create a box layout for the screen
        self.box = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # create the table grid layout
        self.table_rows = 1  # set the number of rows to 10
        self.table = []
        self.table_grid = GridLayout(cols=3, size_hint=(1, None), row_default_height=40, spacing=2)
        self.table_grid.bind(minimum_height=self.table_grid.setter('height'))

        headers = ["Czynność", "Czynność poprzedzająca", "czas trwania"]
        for header in headers:
            label = Label(text=header, size_hint_x=None, width=200)
            self.table_grid.add_widget(label)

        for i in range(self.table_rows):
            row = []
            for j in range(3):
                text = ''
                cell = TextInput(text=text, multiline=False)
                row.append(cell)
                self.table_grid.add_widget(cell)
            self.table.append(row)

        # create a button to add new rows to the table
        add_row_button = Button(text='Add Row', size_hint=(.3, None), height=50)
        add_row_button.bind(on_press=self.add_row)

        # create a submit button to save the values of the text inputs to variables
        submit_button = Button(text='Submit', size_hint=(.3, None), height=50)
        submit_button.bind(on_press=self.submit)

        # create a button to remove the last row from the table
        remove_row_button = Button(text='Remove Row', size_hint=(.3, None), height=50)
        remove_row_button.bind(on_press=self.remove_row)

        # create a button to go back to the HomeScreen
        back_button = Button(text='Go to Home Screen', size_hint=(None, None), size=(150, 50),
                             pos_hint={'right': 1, 'y': 0})
        back_button.bind(on_press=self.go_to_home_screen)

        # create a horizontal box layout for the buttons
        buttons_box = BoxLayout(orientation='horizontal', size_hint=(1, None), height=50, spacing=10)
        buttons_box.add_widget(add_row_button)
        buttons_box.add_widget(remove_row_button)
        buttons_box.add_widget(submit_button)

        # create a scrollable area for the table
        scroll_view = ScrollView(size_hint=(1, 1))
        scroll_view.add_widget(self.table_grid)

        # add the widgets to the screen
        self.box.add_widget(scroll_view)
        self.box.add_widget(buttons_box)
        self.box.add_widget(back_button)
        self.add_widget(self.box)

    def add_row(self, *args):
        self.table_rows += 1
        row = []
        for j in range(3):
            cell = TextInput(multiline=False)
            row.append(cell)
        self.table.append(row)
        for cell in row:
            self.table_grid.add_widget(cell)

    def remove_row(self, instance):
        if self.table_rows > 1:
            # remove the last row from the table grid and table list
            row_to_remove = self.table.pop()
            for cell in row_to_remove:
                self.table_grid.remove_widget(cell)
            self.table_rows -= 1
    def submit(self, instance):
        table_data = []
        for i in range(0, self.table_rows):
            row_values = [cell.text for cell in self.table[i]]
            table_data.append(row_values)

        column_1_data = [row[0] for row in table_data]
        column_2_data = [row[1] for row in table_data]
        column_3_data = []
        for row in table_data:
            try:
                column_3_data.append(float(row[2]))
            except ValueError:
                column_3_data.append(0.0)

        print(column_1_data,column_2_data,column_3_data)
        self.table_data=table_data

        graph_screen = GraphScreen(column_1_data,column_2_data,column_3_data,name='graph')

        screen_manager = self.parent
        screen_manager.add_widget(graph_screen)
        screen_manager.current = 'graph'


    def get_table_data(self):
        return self.table_data
    def go_to_home_screen(self, instance):
        self.manager.current = 'home'

    def go_to_graph(self, instance):
        self.manager.current = 'graph'
class GraphScreen(Screen):
    def __init__(self, col_1_data: List[str], col_2_data: List[str], col_3_data: List[float], **kwargs):
        super().__init__(**kwargs)
        self.result_networks: [Network, ] = None
        self.column_1_data = col_1_data
        self.column_2_data = col_2_data
        self.column_3_data = col_3_data



        nodes_by_id: {Hashable, Node} = self.load_data_from_lists(self.column_1_data,self.column_2_data,self.column_3_data)
        networks: [Network, ] = Solver.solve(nodes_by_activity_id=nodes_by_id)

        button = Button(text='Edit data', size_hint=(None, None), size=(150, 50),
                        pos_hint={'right': 1, 'y': 0})
        button.bind(on_press=self.go_back)
        graph_manager = graph.GraphMeneger(net=networks[0], size=(5000, 5000), size_hint=(None, None))
        self.add_widget(graph_manager)
        self.add_widget(button)

    def load_data_from_user(path: str) -> {Hashable, Node}:
        """ Load data from user.

        @return: dict{Node.id_, Node} - dict of nodes with nodes' id as a key
        """
        nodes: {Hashable, Node} = dict()
        read_data = data_input.load_data_from_file(path=path)
        for id_, prev_ids, duration in read_data[tuple(read_data.keys())[0]]:
            nodes[id_] = Node(id_, prev_ids.split(",") if prev_ids else [], float(duration))
        return nodes

    @staticmethod
    def load_data_from_lists(col1: List[str], col2: List[str], col3: List[float]) -> Dict[Hashable, Node]:
        """ Load data from three lists of strings.

        :param col1: List of strings representing the first column of the data
        :param col2: List of strings representing the second column of the data
        :param col3: List of strings representing the third column of the data
        :return: Dict{Hashable, Node} - Dictionary of nodes with nodes' id as a key
        """
        nodes: Dict[Hashable, Node] = {}
        for id_, prev_ids, duration in zip(col1, col2, col3):
            nodes[id_] = Node(id_, prev_ids.split(",") if prev_ids else [], float(duration))
        return nodes
    def go_back(self, instance):
        self.manager.current = 'table'
        self.manager.remove_widget(self)
