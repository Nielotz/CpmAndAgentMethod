from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
class MyScreenManager(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.transition = NoTransition()
class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        button = Button(text='Go to Other Screen', size_hint=(.2, .1), pos_hint={'right': 1, 'y': 0})
        button2 = Button(text='Go to Table Screen', size_hint=(.2, .1), pos_hint={'center_x': .5, 'center_y': .5})
        button.bind(on_press=self.go_to_other_screen)
        button2.bind(on_press=self.go_to_table_screen)
        self.add_widget(button)
        self.add_widget(button2)

        # add an information label to display messages
        info_label = Label(text='', size_hint=(1, None), height=50)
        self.add_widget(info_label)
        self.ids.info_label = info_label
    def go_to_other_screen(self, instance):
        self.manager.current = 'other'
    def go_to_table_screen(self, instance):
        self.manager.current = 'table'


class OtherScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        button = Button(text='Go to Home Screen', size_hint=(.2, .1), pos_hint={'right': 1, 'y': 0})
        button.bind(on_press=self.go_to_home_screen)
        self.add_widget(button)

    def go_to_home_screen(self, instance):
        self.manager.current = 'home'


class TableScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # create a box layout for the screen
        box = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # create a label for the screen title
        title_label = Label(text='Table Screen', font_size=24)

        # create a button to go back to the HomeScreen
        back_button = Button(text='Go to Home Screen', size_hint=(None, None), size=(150, 50),
                             pos_hint={'right': 1, 'y': 0})
        back_button.bind(on_press=self.go_to_home_screen)

        # create the table grid layout
        self.table_rows = 10  # set the number of rows to 10
        self.table = []
        self.table_grid = GridLayout(cols=3, size_hint=(1, None), row_default_height=40, spacing=2)
        self.table_grid.bind(minimum_height=self.table_grid.setter('height'))

        headers = ["Czynność", "Czas trwania", "Następstwo Zdarzeń"]
        for header in headers:
            label = Label(text=header, size_hint_x=None, width=200)
            self.table_grid.add_widget(label)

        for i in range(self.table_rows):
            row = []
            for j in range(3):
                if i == 0:
                    text = headers[j]
                else:
                    text = ''
                cell = TextInput(text=text, multiline=False)
                row.append(cell)
                self.table_grid.add_widget(cell)
            self.table.append(row)

        # create a button to add new rows to the table
        add_row_button = Button(text='Add Row', size_hint=(None, None), size=(150, 50),
                                pos_hint={'center_x': .5, 'center_y': .5})
        add_row_button.bind(on_press=self.add_row)

        # create a scrollable area for the table
        scroll_view = ScrollView(size_hint=(1, 1))
        scroll_view.add_widget(self.table_grid)

        # create a submit button to save the values of the text inputs to variables
        submit_button = Button(text='Submit', size_hint=(None, None), size=(150, 50),
                               pos_hint={'center_x': .5, 'center_y': .5})
        submit_button.bind(on_press=self.submit)


        # add the widgets to the screen
        box.add_widget(title_label)
        box.add_widget(back_button)
        box.add_widget(scroll_view)
        box.add_widget(add_row_button)
        box.add_widget(submit_button)
        self.add_widget(box)

    def add_row(self, *args):
        self.table_rows += 1
        row = []
        for j in range(3):
            cell = TextInput(multiline=False)
            row.append(cell)
        self.table.append(row)
        for cell in row:
            self.table_grid.add_widget(cell)

    def submit(self, instance):
        for i in range(1, self.table_rows):
            row_values = [cell.text for cell in self.table[i]]

            # check if the edited row is complete
            if any(cell.focus for cell in self.table[i]):
                if not all(row_values):
                    # display a message that all fields in the edited row need to be filled
                    self.manager.current_screen.ids.info_label.text = "All fields in the edited row need to be filled"
                    return

    def go_to_home_screen(self, instance):
        self.manager.current = 'home'

class MyApp(App):
    def build(self):
        sm = MyScreenManager()
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(OtherScreen(name='other'))
        sm.add_widget(TableScreen(name='table'))
        return sm


MyApp().run()