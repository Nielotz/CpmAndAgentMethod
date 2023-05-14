import os
from typing import Hashable, List, Dict, Optional

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.utils import get_color_from_hex

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
        self.add_widget(AgentHomeScreen(name='agentHome'))
        self.add_widget(AgentManualInput(name='ami'))


class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        box = BoxLayout(orientation='horizontal', padding=10, spacing=10)
        cpmButton = Button(text='CPM method', size_hint=(.2, .1), pos_hint={'center_x': .5, 'center_y': .5})
        cpmButton.bind(on_press=self.go_to_cpm_home_screen)
        agentButton = Button(text='Agent method', size_hint=(.2, .1), pos_hint={'center_x': .5, 'center_y': .5})
        agentButton.bind(on_press=self.go_to_agent_home_screen)
        box.add_widget(cpmButton)
        box.add_widget(agentButton)
        self.add_widget(box)

        # add an information label to display messages
        info_label = Label(text='Logistic Simulator', size_hint=(1, None), pos_hint={'top': 1}, height=100,
                           color=(0, 0, 0, 1), font_size=30)
        self.add_widget(info_label)
        self.ids.info_label = info_label

    def go_to_cpm_home_screen(self, instance):
        self.manager.current = 'cpmHome'
    def go_to_agent_home_screen(self, instance):
        self.manager.current = 'agentHome'

class CpmHomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # create a box layout for the screen
        box = BoxLayout(orientation='vertical', padding=10, spacing=10)
        input_data_button = Button(text='Input Data to table', size_hint=(.3, None), pos_hint={'left': 1, 'y': 0})
        read_data_button = Button(text='Input Data from file', size_hint=(.3, None), pos_hint={'left': 1, 'y': 0})
        input_data_button.bind(on_press=self.go_to_table_screen)
        read_data_button.bind(on_press=self.open_filechooser_popup)

        # create a horizontal box layout for the buttons
        buttons_box = BoxLayout(orientation='horizontal', size_hint=(1, None), height=50, spacing=10)
        buttons_box.add_widget(input_data_button)
        buttons_box.add_widget(read_data_button)
        box.add_widget(buttons_box)
        self.add_widget(box)

        # create button for backing to previous screen
        back_arrow = Button(text='<', pos_hint={'left': 1, 'top': 1}, size_hint=(None, None), size=(15, 15))
        back_arrow.bind(on_press=self.go_back_arrow)

        # add an information label to display messages
        info_label = Label(text='Choose form of data input', size_hint=(1, None), pos_hint={'top': 1}, height=100,
                           color=(0, 0, 0, 1), font_size=30)
        self.add_widget(info_label)
        self.ids.info_label = info_label
        self.add_widget(back_arrow)

    def go_to_table_screen(self, instance):
        self.manager.current = 'table'

    def go_back_arrow(self, instance):
        self.manager.current = 'home'

    def open_filechooser_popup(self, instance):
        # create a popup window
        popup = Popup(title='Choose a file', size_hint=(0.9, 0.9), auto_dismiss=False)

        # create a custom title bar with an "X" button
        box = BoxLayout(size_hint=(1, None), height=50, spacing=10, pos_hint={'x': 0.97, 'y': 1})
        close_button = Button(text='X', size_hint=(None, None), size=(10, 10), pos_hint={'x': 0, 'y': 1.4})
        close_button.bind(on_press=popup.dismiss)
        box.add_widget(close_button)

        # create a filechooser widget
        filechooser = FileChooserListView()
        filechooser.path = os.getcwd()  # set the initial path to the current directory
        filechooser.filters = ['*.txt']  # only show .txt files

        # add the title bar and filechooser widget to a container layout
        container = BoxLayout(orientation='vertical')
        container.add_widget(box)
        container.add_widget(filechooser)

        # add the container layout as the content of the popup
        popup.content = container

        # create a callback function to handle the file selection
        def on_selection(instance_, selected_file):
            try:
                # check if the file format is supported
                if not selected_file[0].endswith('.txt'):
                    raise Exception('File format not supported')

                # create object of graph_screen giving him selected file
                print(selected_file[0])
                popup.dismiss()
                graph_screen = GraphScreen(None, None, None, selected_file[0], name='graph')

                screen_manager = self.parent
                screen_manager.add_widget(graph_screen)
                screen_manager.current = 'graph'
            except Exception as e:
                # display an error message to the user
                error_popup = Popup(title='File format not supported', content=Label(text=str(selected_file)),
                                    size_hint=(0.8, 0.3), auto_dismiss=True)
                error_popup.open()

        # bind the selection callback to the filechooser widget
        filechooser.bind(selection=on_selection)

        # open the popup
        popup.open()

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

        headers = ["Action", "Preceding action", "Duration"]
        for header in headers:
            label = Label(text=header, size_hint_x=None, width=200, color=(0, 0, 0, 1))
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
        back_arrow = Button(text='<', pos_hint={'left': 1, 'top': 1}, size_hint=(None, None), size=(15, 15))
        back_arrow.bind(on_press=self.go_back_arrow)

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
        self.add_widget(back_arrow)
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
        try:
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

            if '' in column_1_data or 0.0 in column_3_data:
                # Turn the fields red
                for i in range(len(self.table)):
                    if self.table[i][0].text == '':
                        self.table[i][0].background_color = get_color_from_hex('#d3212d')  # amaranth red
                    if self.table[i][2].text == '':
                        self.table[i][2].background_color = get_color_from_hex('#d3212d')  # amaranth red

                # Show the pop-up message
                popup_message = 'Please fill correct data in the first and third columns.'
                popup = Popup(title='Error', content=Label(text=popup_message), size_hint=(None, None), size=(400, 400))
                popup.open()
            else:
                # Reset the fields' background color
                for i in range(len(self.table)):
                    self.table[i][0].background_color = (1, 1, 1, 1)  # white
                    self.table[i][2].background_color = (1, 1, 1, 1)  # white
                print(column_1_data, column_2_data, column_3_data)
                self.table_data = table_data
                graph_screen = GraphScreen(column_1_data, column_2_data, column_3_data, name='graph')

                screen_manager = self.parent
                screen_manager.add_widget(graph_screen)
                screen_manager.current = 'graph'
        except Exception as e:
            # display an error message to the user
            error_popup = Popup(title='Error', content=Label(text='Graph cannot be made from this data'),
                                size_hint=(0.8, 0.3), auto_dismiss=True)
            error_popup.open()

    def get_table_data(self):
        return self.table_data

    def go_back_arrow(self, instance):
        self.manager.current = 'cpmHome'

    def go_to_graph(self, instance):
        self.manager.current = 'graph'

class GraphScreen(Screen):
    def __init__(self,
                 col_1_data: Optional[list[str]], col_2_data: Optional[list[str]], col_3_data: Optional[list[float]],
                 path: Optional[str] = None, **kwargs):
        super().__init__(**kwargs)
        self.result_networks: [Network, ] = None
        self.column_1_data = col_1_data
        self.column_2_data = col_2_data
        self.column_3_data = col_3_data
        self.path = path

        def load_data_from_user(path_: str) -> {Hashable, Node}:
            """ Load data from user.

            @return: dict{Node.id_, Node} - dict of nodes with nodes' id as a key
            """
            nodes: {Hashable, Node} = dict()
            read_data = data_input.load_data_from_file(path=path_)
            for id_, prev_ids, duration in read_data[tuple(read_data.keys())[0]]:
                nodes[id_] = Node(id_, prev_ids.split(",") if prev_ids else [], float(duration))
            return nodes

        if path is None:
            nodes_by_id: {Hashable, Node} = self.load_data_from_lists(self.column_1_data, self.column_2_data,
                                                                      self.column_3_data)
            button = Button(text='Edit data', size_hint=(None, None), size=(150, 50),
                            pos_hint={'right': 1, 'y': 0})
            button.bind(on_press=self.go_back_to_table)
        else:
            nodes_by_id: {Hashable, Node} = load_data_from_user(path_=path)
            button = Button(text='Edit data', size_hint=(None, None), size=(150, 50),
                            pos_hint={'right': 1, 'y': 0})
            button.bind(on_press=self.go_back_to_home)

        networks: [Network, ] = Solver.solve(nodes_by_activity_id=nodes_by_id)

        graph_manager = graph.GraphManager(nets=networks, size=(5000, 5000), size_hint=(None, None))
        self.add_widget(graph_manager)
        self.add_widget(button)

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

    def go_back_to_table(self, instance):
        self.manager.current = 'table'
        self.manager.remove_widget(self)

    def go_back_to_home(self, instance):
        self.manager.current = 'cpmHome'
        self.manager.remove_widget(self)

class AgentHomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # create a box layout for the screen
        box = BoxLayout(orientation='vertical', padding=10, spacing=10)
        input_data_button = Button(text='Input Data manually', size_hint=(.3, None), pos_hint={'left': 1, 'y': 0})
        input_data_button.bind(on_press=self.go_to_manual_input)
        read_data_button = Button(text='Input Data from file', size_hint=(.3, None), pos_hint={'left': 1, 'y': 0})
        read_data_button.bind(on_press=self.open_filechooser_popup)

        # create a horizontal box layout for the buttons
        buttons_box = BoxLayout(orientation='horizontal', size_hint=(1, None), height=50, spacing=10)
        buttons_box.add_widget(input_data_button)
        buttons_box.add_widget(read_data_button)
        box.add_widget(buttons_box)
        self.add_widget(box)

        # create button for backing to previous screen
        back_arrow = Button(text='<', pos_hint={'left': 1, 'top': 1}, size_hint=(None, None), size=(15, 15))
        back_arrow.bind(on_press=self.go_back_arrow)

        # add an information label to display messages
        info_label = Label(text='Choose form of data input', size_hint=(1, None), pos_hint={'top': 1}, height=100,
                           color=(0, 0, 0, 1), font_size=30)
        self.add_widget(info_label)
        self.ids.info_label = info_label
        self.add_widget(back_arrow)


    def go_back_arrow(self, instance):
        self.manager.current = 'home'
    def go_to_manual_input(self, instance):
        self.manager.current = 'ami'
    def open_filechooser_popup(self, instance):
        # create a popup window
        popup = Popup(title='Choose a file', size_hint=(0.9, 0.9), auto_dismiss=False)

        # create a custom title bar with an "X" button
        box = BoxLayout(size_hint=(1, None), height=50, spacing=10, pos_hint={'x': 0.97, 'y': 1})
        close_button = Button(text='X', size_hint=(None, None), size=(10, 10), pos_hint={'x': 0, 'y': 1.4})
        close_button.bind(on_press=popup.dismiss)
        box.add_widget(close_button)

        # create a filechooser widget
        filechooser = FileChooserListView()
        filechooser.path = os.getcwd()  # set the initial path to the current directory
        filechooser.filters = ['*.txt']  # only show .txt files

        # add the title bar and filechooser widget to a container layout
        container = BoxLayout(orientation='vertical')
        container.add_widget(box)
        container.add_widget(filechooser)

        # add the container layout as the content of the popup
        popup.content = container

        # create a callback function to handle the file selection
        def on_selection(instance_, selected_file):
            try:
                # check if the file format is supported
                if not selected_file[0].endswith('.txt'):
                    raise Exception('File format not supported')

                # TODO Do something with file
                print(selected_file[0])
                todo_popup = Popup(title='TODO', content=Label(text='Not Yet Working'),
                                    size_hint=(0.8, 0.3), auto_dismiss=True)
                todo_popup.open()
                popup.dismiss()
            except Exception as e:
                # display an error message to the user
                error_popup = Popup(title='File format not supported', content=Label(text=str(selected_file)),
                                    size_hint=(0.8, 0.3), auto_dismiss=True)
                error_popup.open()

        # bind the selection callback to the filechooser widget
        filechooser.bind(selection=on_selection)

        # open the popup
        popup.open()

class AgentManualInput(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # create button for backing to previous screen
        back_arrow = Button(text='<', pos_hint={'left': 1, 'top': 1}, size_hint=(None, None), size=(15, 15))
        back_arrow.bind(on_press=self.go_back_arrow)

        demand_supply_button = Button(text='set Supply/Demand')
        supplier_receiver_button = Button(text='add Supplier/Receiver')
        costs_table_button = Button(text='Costs table')
        bl = BoxLayout(orientation='vertical', size_hint=(0.25, None), spacing=10, pos_hint={'center_x': 0.5, 'center_y': 0.5})
        bl.add_widget(demand_supply_button)
        bl.add_widget(supplier_receiver_button)
        bl.add_widget(costs_table_button)


        self.add_widget(back_arrow)
        self.add_widget(bl)
    def go_back_arrow(self, instance):
        self.manager.current = 'agentHome'
    def go_supply_demand