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
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from kivy.utils import get_color_from_hex
from kivy.uix.checkbox import CheckBox

import data_input
import gui.graph as graph
from cpm.network.network import Network
from cpm.node import Node
from cpm.solver import Solver
from agent.data_loader import load_data_from_json_file, load_data_from_gui
from agent.supply_chain import SupplyChainData
from agent.agent import Agent

import gui.agent_out as ao
class LabeledTextInput(BoxLayout):
    def __init__(self, label_text='', input_type='text', multiline=False, **kwargs):
        super(LabeledTextInput, self).__init__(**kwargs)

        self.orientation = 'horizontal'
        self.spacing = 10

        self.label = Label(text=label_text)
        self.text_input = TextInput(input_type=input_type, multiline=multiline)

        self.add_widget(self.label)
        self.add_widget(self.text_input)

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
        box = BoxLayout(orientation='vertical', size_hint=(0.25, None), spacing=10, pos_hint={'center_x': 0.5, 'center_y': 0.5})
        cpmButton = Button(text='CPM method')
        cpmButton.bind(on_press=self.go_to_cpm_home_screen)
        agentButton = Button(text='Agent method')
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

        input_data_button = Button(text='Input Data to table')
        read_data_button = Button(text='Input Data from file')
        input_data_button.bind(on_press=self.go_to_table_screen)
        read_data_button.bind(on_press=self.open_filechooser_popup)

        buttons_box = BoxLayout(orientation='vertical', size_hint=(0.25, None), spacing=10, pos_hint={'center_x': 0.5, 'center_y': 0.5})
        buttons_box.add_widget(input_data_button)
        buttons_box.add_widget(read_data_button)

        self.add_widget(buttons_box)

        # create button for backing to previous screen
        back_arrow = Button(text='<', pos_hint={'left': 1, 'top': 1}, size_hint=(None, None), size=(15, 15))
        back_arrow.bind(on_press=self.go_back_arrow)

        # add an information label to display messages
        info_label = Label(text='Choose form of data input for CPM', size_hint=(1, None), pos_hint={'top': 1}, height=100,
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

        input_data_button = Button(text='Input Data manually')
        input_data_button.bind(on_press=self.go_to_manual_input)
        read_data_button = Button(text='Input Data from file')
        read_data_button.bind(on_press=self.open_filechooser_popup)

        # create a vertical box layout for the buttons
        buttons_box = BoxLayout(orientation='vertical', size_hint=(0.25, None), spacing=10, pos_hint={'center_x': 0.5, 'center_y': 0.5})
        buttons_box.add_widget(input_data_button)
        buttons_box.add_widget(read_data_button)
        self.add_widget(buttons_box)

        # create button for backing to previous screen
        back_arrow = Button(text='<', pos_hint={'left': 1, 'top': 1}, size_hint=(None, None), size=(15, 15))
        back_arrow.bind(on_press=self.go_back_arrow)

        # add an information label to display messages
        info_label = Label(text='Choose form of data input for agent method', size_hint=(1, None), pos_hint={'top': 1}, height=100,
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
        filechooser.filters = ['*.json']  # only show .json files

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
                if not selected_file[0].endswith('.json'):
                    raise Exception('File format not supported')

                print(selected_file[0])
                supply_chain_data, _ = load_data_from_json_file(path=selected_file[0])
                supply_chain_data: SupplyChainData

                result = Agent.solve(supply_chain_data=supply_chain_data)
                agentScreen = AgentOutput(result, name='ao')
                screen_manager = self.parent
                screen_manager.add_widget(agentScreen)
                screen_manager.current = 'ao'
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

        # create instance variables for supply and demand
        self.suppliers = 0
        self.receivers = 0
        self.supply = []
        self.demand = []
        self.buy = []
        self.sell = []
        self.transport_table = [[]]
        self.fictional = False

        # create button for backing to previous screen
        back_arrow = Button(text='<', pos_hint={'left': 1, 'top': 1}, size_hint=(None, None), size=(15, 15))
        back_arrow.bind(on_press=self.go_back_arrow)

        demand_supply_button = Button(text='set Supply/Demand')
        demand_supply_button.bind(on_press=self.add_supply_demand)

        supplier_receiver_button = Button(text='add Supplier/Receiver')
        supplier_receiver_button.bind(on_press=self.add_supplier_receiver)

        buy_sell_button = Button(text='set Sell/Buy costs')
        buy_sell_button.bind(on_press=self.add_buy_sell_costs)

        transport_costs_table_button = Button(text='Transportation costs table')
        transport_costs_table_button.bind(on_press=self.add_trans_costs)

        save_all_button = Button(text='Save All Data', pos_hint={'right': 1, 'bottom': 1}, size_hint=(None, None), size=(100, 50))
        save_all_button.bind(on_press=self.save_all_data)

        checkbox = CheckBox(active=self.fictional, color=(1,0,0,1), pos_hint={'x': 0.015, 'bottom': 1}, size_hint=(None, None))
        checkbox.bind(active=self.on_checkbox_active)
        checkbox_backgr = Button(text="Toggle Fictional", pos_hint={'left': 1, 'bottom': 1}, size_hint=(None, None), disabled=True,size=(130, 70), color=(1,0,0,1))

        bl = BoxLayout(orientation='vertical', size_hint=(0.25, None), spacing=10, pos_hint={'center_x': 0.5, 'center_y': 0.5}, height=300)
        bl.add_widget(supplier_receiver_button)
        bl.add_widget(demand_supply_button)
        bl.add_widget(buy_sell_button)
        bl.add_widget(transport_costs_table_button)

        self.add_widget(back_arrow)
        self.add_widget(save_all_button)
        self.add_widget(checkbox_backgr)
        self.add_widget(checkbox)
        self.add_widget(bl)
    def on_checkbox_active(self, checkbox, value):
        if value:
            self.fictional = value
        else:
            self.fictional = False
        print(f'Fictional: {self.fictional}')
    def go_back_arrow(self, instance):
        self.manager.current = 'agentHome'
    def add_supply_demand(self, instance):
        if self.suppliers != 0 and self.receivers != 0:
            content = BoxLayout(
                orientation='vertical',
                spacing=10,
                padding=10,
                size_hint=(None, None),
                size=(500, 300)
            )

            input_layout = BoxLayout(
                orientation='horizontal',
                spacing=10,
                size_hint=(None, None),
                size=(400, 300),
                pos_hint={'left':1}
            )

            supply_layout = GridLayout(
                cols=1,
                spacing=10,
                size_hint=(None, None),
                width=150,
                pos_hint={'left': 1}
            )
            supply_layout.bind(minimum_height=supply_layout.setter('height'))

            # create input fields
            supply_label = Label(text='Supply values:', size_hint=(1, None), height=30)
            supply_layout.add_widget(supply_label)

            # create text inputs for each supplier
            supply_inputs = []
            for i in range(self.suppliers):
                suppliers_label_text = 'S' + str(i + 1)  # Convert i to a string and concatenate with 'S'
                supply_input = LabeledTextInput(
                    label_text=suppliers_label_text,
                    input_type='number',
                    size_hint=(1, None),
                    height=30,
                    multiline=False
                )
                if i < len(self.supply):
                    supply_input.text_input.text = str(self.supply[i])
                supply_layout.add_widget(supply_input)
                supply_inputs.append(supply_input)

            supply_scroll = ScrollView(size_hint=(1, None), size=(200, 160), pos_hint={'left': 1})
            supply_scroll.add_widget(supply_layout)
            input_layout.add_widget(supply_scroll)

            demand_layout = GridLayout(
                cols=1,
                spacing=10,
                size_hint=(None, None),
                width=150,
                pos_hint={'left': 1}
            )
            demand_layout.bind(minimum_height=demand_layout.setter('height'))

            # create input fields
            demand_label = Label(text='Demand values:', size_hint=(1, None), height=30)
            demand_layout.add_widget(demand_label)

            # create text inputs for each supplier
            demand_inputs = []
            for i in range(self.receivers):
                receivers_label_text = 'R' + str(i + 1)  # Convert i to a string and concatenate with 'S'
                demand_input = LabeledTextInput(
                    label_text=receivers_label_text,
                    input_type='number',
                    size_hint=(1, None),
                    height=30,
                    multiline=False
                )
                if i < len(self.demand):
                    demand_input.text_input.text = str(self.demand[i])
                demand_layout.add_widget(demand_input)
                demand_inputs.append(demand_input)

            demand_scroll = ScrollView(size_hint=(1, None), size=(200, 160), pos_hint={'left': 1})
            demand_scroll.add_widget(demand_layout)
            input_layout.add_widget(demand_scroll)

            content.add_widget(input_layout)

            # create a submit button to save the values
            submit_button = Button(text='Submit', size_hint=(None, None), size=(100, 50))
            content.add_widget(submit_button)

            # create the popup with the content and open it
            popup = Popup(
                title='Set Supply/Demand',
                content=content,
                size_hint=(None, None),
                size=(450, 300),
                pos_hint={'top': 0.95}
            )
            submit_button.bind(on_press=lambda x: self.save_supply_demand(popup, supply_inputs, demand_inputs))
            popup.open()
        else:
            popup = Popup(
                title='Error',
                content=Label(text='Set suppliers and receivers first'),
                size_hint=(None, None),
                size=(500, 300)
            )
            popup.open()
    def save_supply_demand(self, popup, supply_inputs, demand_inputs):
        try:
            # retrieve the values from the text inputs and save them
            self.supply = []
            self.demand = []
            for input_field in supply_inputs:
                self.supply.append(int(input_field.text_input.text))
            for input_field in demand_inputs:
                self.demand.append(int(input_field.text_input.text))

            # close the popup
            popup.dismiss()

            # do something with the supply values
            print(f'Supply: {self.supply}, Demand: {self.demand}')
        except Exception as e:
            # display an error message to the user
            error_popup = Popup(
                title='ERROR',
                content=Label(text='Inputted value must be an integer'),
                size_hint=(0.8, 0.3),
                auto_dismiss=True
            )
            error_popup.open()
    def add_supplier_receiver(self, instance):
        # create a popup window
        content = BoxLayout(orientation='vertical', spacing=10, padding=10, size_hint=(None, None), size=(300, 200))
        spinner_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint=(None, None), size=(300, 50))

        # create two vertical BoxLayouts for supplier and receiver labels and spinners
        supplier_box = BoxLayout(orientation='vertical', spacing=5, size_hint=(0.5, None), height=50)
        receiver_box = BoxLayout(orientation='vertical', spacing=5, size_hint=(0.5, None), height=50)

        supplier_label = Label(text='Suppliers:', size_hint=(1, None), height=30)
        receiver_label = Label(text='Receivers:', size_hint=(1, None), height=30)

        supplier_spinner = Spinner(values=('1', '2', '3', '4', '5', '6', '7', '8', '9', '10'), size_hint=(1, None), height=30)
        receiver_spinner = Spinner(values=('1', '2', '3', '4', '5', '6', '7', '8', '9', '10'), size_hint=(1, None), height=30)

        # pre-populate the spinners with the previous values
        supplier_spinner.text = str(self.suppliers)
        receiver_spinner.text = str(self.receivers)

        supplier_box.add_widget(supplier_label)
        supplier_box.add_widget(supplier_spinner)
        receiver_box.add_widget(receiver_label)
        receiver_box.add_widget(receiver_spinner)

        spinner_layout.add_widget(supplier_box)
        spinner_layout.add_widget(receiver_box)

        content.add_widget(spinner_layout)

        # create a submit button to save the values
        submit_button = Button(text='Submit', size_hint=(None, None), size=(100, 50))
        content.add_widget(submit_button)

        popup = Popup(title='Set Supplier/Receiver count', content=content, size_hint=(None, None), size=(400, 200), pos_hint={'top': 0.95})
        # bind the buttons to actions
        submit_button.bind(on_press=lambda x: self.save_suppliers_receivers(popup, supplier_spinner, receiver_spinner))
        popup.open()
    def save_suppliers_receivers(self, popup, supplier_spinner, receiver_spinner):
        # retrieve the values from the text inputs and save them
        self.suppliers = int(supplier_spinner.text)
        self.receivers = int(receiver_spinner.text)

        # close the popup
        popup.dismiss()

        # do something with the supply and demand values
        print(f'Suppliers: {self.suppliers}, Receivers: {self.receivers}')
    def add_buy_sell_costs(self, instance):
        if self.suppliers != 0 and self.receivers != 0:
            content = BoxLayout(
                orientation='vertical',
                spacing=10,
                padding=10,
                size_hint=(None, None),
                size=(500, 300)
            )

            input_layout = BoxLayout(
                orientation='horizontal',
                spacing=10,
                size_hint=(None, None),
                size=(400, 300),
                pos_hint={'left': 1}
            )

            buy_layout = GridLayout(
                cols=1,
                spacing=10,
                size_hint=(None, None),
                width=150
            )
            buy_layout.bind(minimum_height=buy_layout.setter('height'))

            buy_label = Label(text='Buy costs:', size_hint=(1, None), height=30)
            buy_layout.add_widget(buy_label)

            # create text inputs for each supplier
            buy_inputs = []
            for i in range(self.suppliers):
                suppliers_label_text = 'S' + str(i + 1)
                buy_input = LabeledTextInput(
                    label_text=suppliers_label_text,
                    input_type='number',
                    size_hint=(1, None),
                    height=30,
                    multiline=False
                )
                if i < len(self.buy):
                    buy_input.text_input.text = str(self.buy[i])
                buy_layout.add_widget(buy_input)
                buy_inputs.append(buy_input)

            buy_scroll = ScrollView(size_hint=(1, None), size=(200, 160), pos_hint={'center_x': 0.5})

            sell_layout = GridLayout(
                cols=1,
                spacing=10,
                size_hint=(None, None),
                width=150
            )
            sell_layout.bind(minimum_height=sell_layout.setter('height'))

            # create input fields
            sell_label = Label(text='Sell costs:', size_hint=(1, None), height=30)
            sell_layout.add_widget(sell_label)

            # create text inputs for each receiver
            sell_inputs = []
            for i in range(self.receivers):
                receivers_label_text = 'R' + str(i + 1)  # Convert i to a string and concatenate with 'S'
                sell_input = LabeledTextInput(
                    label_text=receivers_label_text,
                    input_type='number',
                    size_hint=(1, None),
                    height=30,
                    multiline=False
                )
                if i < len(self.sell):
                    sell_input.text_input.text = str(self.sell[i])
                sell_layout.add_widget(sell_input)
                sell_inputs.append(sell_input)

            sell_scroll = ScrollView(size_hint=(1, None), size=(200, 160), pos_hint={'center_x': 0.5})

            buy_scroll.add_widget(buy_layout)
            input_layout.add_widget(buy_scroll)
            sell_scroll.add_widget(sell_layout)
            input_layout.add_widget(sell_scroll)

            content.add_widget(input_layout)

            # create a submit button to save the values
            submit_button = Button(text='Submit', size_hint=(None, None), size=(100, 50))
            content.add_widget(submit_button)

            # create the popup with the content and open it
            popup = Popup(
                title='Set Sell/Buy costs',
                content=content,
                size_hint=(None, None),
                size=(450, 300),
                pos_hint={'top': 0.95}
            )
            submit_button.bind(on_press=lambda x: self.save_buy_sell(popup, buy_inputs, sell_inputs))
            popup.open()
        else:
            popup = Popup(
                title='Error',
                content=Label(text='Set suppliers and receivers first'),
                size_hint=(None, None),
                size=(400, 200)
            )
            popup.open()
    def save_buy_sell(self, popup, buy_inputs, sell_inputs):
        try:
            # retrieve the values from the text inputs and save them
            self.sell = []
            self.buy = []
            for input_field in buy_inputs:
                self.buy.append(int(input_field.text_input.text))
            for input_field in sell_inputs:
                self.sell.append(int(input_field.text_input.text))

            # close the popup
            popup.dismiss()

            # do something with the supply values
            print(f'Buy costs: {self.buy}, Sell costs: {self.sell}')
        except Exception as e:
            # display an error message to the user
            error_popup = Popup(
                title='ERROR',
                content=Label(text='Inputted value must be an integer'),
                size_hint=(0.8, 0.3),
                auto_dismiss=True
            )
            error_popup.open()
    def add_trans_costs(self, instance):
        if self.suppliers != 0 and self.receivers != 0:
            # Create the table layout
            table_layout = BoxLayout(orientation='vertical', pos_hint={'top': 1, 'left': 1})

            # Add the header row with receiver numbers
            header_layout = BoxLayout(orientation='horizontal', size_hint=(1, None), height=30)
            header_layout.add_widget(Label(text=''))  # Empty label for the top-left cell
            for receiver in range(1, self.receivers + 1):
                header_layout.add_widget(Label(text=f'R{receiver}'))
            table_layout.add_widget(header_layout)

            # Add the rows with supplier numbers and transportation costs
            self.costs_inputs = []  # Store the TextInput objects in a list
            for supplier in range(1, self.suppliers + 1):
                row_layout = BoxLayout(orientation='horizontal', size_hint=(1, None), height=30)
                row_layout.add_widget(
                    Label(text=f'S{supplier}', size_hint=(None, None), width=80, height=30))  # Label for the supplier
                for receiver in range(1, self.receivers + 1):
                    # Create a text input field for each transportation cost
                    costs_input = TextInput()
                    self.costs_inputs.append(costs_input)  # Add the TextInput object to the list

                    # Prepopulate the text input with value from transport_table if available
                    if supplier <= len(self.transport_table) and receiver <= len(self.transport_table[supplier - 1]):
                        costs_input.text = str(self.transport_table[supplier - 1][receiver - 1])

                    row_layout.add_widget(costs_input)
                table_layout.add_widget(row_layout)

            # Add the submit button
            submit_button = Button(text='Submit', size_hint=(None, None), size=(100, 40))
            table_layout.add_widget(submit_button)
            label = Label()
            table_layout.add_widget(label)
            popup = Popup(
                title='Transportation costs table',
                content=table_layout,
                size_hint=(None, None),
                size=(700, 500)
            )
            submit_button.bind(on_press=lambda x: self.save_trans_costs(popup))
            popup.open()
        else:
            popup = Popup(
                title='Error',
                content=Label(text='Set suppliers and receivers first'),
                size_hint=(None, None),
                size=(400, 200)
            )
            popup.open()
    def save_trans_costs(self, popup):
        try:
            self.transport_table = [[] for _ in range(self.suppliers)]
            index = 0
            for supplier in range(self.suppliers):
                for receiver in range(self.receivers):
                    # Get the text input corresponding to the current row and column
                    text_input = self.costs_inputs[index]
                    # Append the inputted value to the transport table cell
                    self.transport_table[supplier].append(int(text_input.text))
                    index += 1
            # Close the popup
            popup.dismiss()
            print(f'Transport costs: {self.transport_table}')
        except ValueError:
            # Display an error message to the user
            error_popup = Popup(
                title='ERROR',
                content=Label(text='Inputted value must be an integer'),
                size_hint=(0.8, 0.3),
                auto_dismiss=True
            )
            error_popup.open()
    def save_all_data(self, instance):
        try:
            if(self.suppliers == 0 or self.receivers ==0 or self.supply == 0 or self.demand ==0 or self.sell ==0 or self.buy==0 or self.transport_table == 0):
                raise ValueError

            print(f'Suppliers: {self.suppliers}\n'
                  f'Receivers: {self.receivers}\n'
                  f'Supply: {self.supply}\n'
                  f'Demand: {self.demand}\n'
                  f'Buy costs: {self.buy}\n'
                  f'Sell costs: {self.sell}\n'
                  f'Transport costs: {self.transport_table}\n'
                  f'Fictional: {self.fictional}')

            supply_chain_data = load_data_from_gui(self.supply, self.demand, self.sell, self.buy, self.transport_table, self.fictional)
            supply_chain_data: SupplyChainData
            result = Agent.solve(supply_chain_data=supply_chain_data)
            agentScreen = AgentOutput(result, name='ao')
            screen_manager = self.parent
            screen_manager.add_widget(agentScreen)
            screen_manager.current = 'ao'
        except Exception as e:
            # display an error message to the user
            error_popup = Popup(
                title='ERROR',
                content=Label(text='Something went wrong'),
                size_hint=(0.8, 0.3),
                auto_dismiss=True
            )
            error_popup.open()
class AgentOutput(Screen):
    def __init__(self, agentData, **kwargs):
        super().__init__(**kwargs)
        agentOutput = ao.AgentManager(agentData)

        self.add_widget(agentOutput)

        # create button for backing to previous screen
        back_arrow = Button(text='<', pos_hint={'left': 1, 'top': 1}, size_hint=(None, None), size=(15, 15))
        back_arrow.bind(on_press=self.go_back_arrow)
        self.add_widget(back_arrow)
    def go_back_arrow(self, instance):
        self.manager.current='ami'
        self.manager.remove_widget(self)






