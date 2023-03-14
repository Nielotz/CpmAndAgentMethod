from typing import Any

from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.layout import Layout
from kivy.uix.scrollview import ScrollView
from kivy.uix.stacklayout import StackLayout
from kivy.uix.widget import Widget


class Header(Button):
    def __init__(self, **kwargs):
        super().__init__(size_hint_max_y=30, **kwargs)


class Cell(Label):
    def __init__(self, **kwargs):
        super().__init__(size_hint_max_y=30, **kwargs)


class Column(StackLayout):
    def __init__(self, header: str, **kwargs):
        super().__init__(orientation='lr-tb', size_hint_x=1, **kwargs)
        self.cells: [Cell, ] = []
        self.header: Header = Header(text=header)

        self.add_widget(self.header)
        # self.add_widget(self.cells[0])
        # self.add_widget(self.cells[1])

    def add_cell(self, value: Any):
        self.cells.append(cell := Cell(text=value))  # , multiline=False
        self.add_widget(cell)

class Table(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="horizontal", **kwargs)
        self.columns: [Column, ] = []

        self.spacer: Widget = Widget()

    def add_column(self, header: str):
        self.columns.append(column := Column(header=header))
        self.add_widget(column)

    def add_values(self, row: [Any, ]):
        print(f"[DEBUG] Adding row: {row}")
        if len(row) != len(self.columns):
            print("[WARNING] Amount of values does not match number of columns!")
            print(f"          values ({len(row)}): {row}")
            print(f"          columns ({len(self.columns)}): {[col.header.text for col in self.columns]}")

        for value, target_col in zip(row, self.columns):
            target_col.add_cell(value)


class OutputTable(Table):
    def __init__(self, headers: [], **kwargs):
        super().__init__(**kwargs)
        for header in headers:
            self.add_column(header=header)
