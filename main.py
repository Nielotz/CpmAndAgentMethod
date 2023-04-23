from typing import Hashable

from kivy.app import App
from kivy.core.window import Window

import data_input
import gui.graph as graph
from gui.screen_manager import *
from cpm.network.network import Network
from cpm.node import Node
from cpm.solver import Solver




class CPMapp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.result_networks: [Network, ] = None

    @staticmethod
    def load_data_from_user(path: str) -> {Hashable, Node}:
        """ Load data from user.

        @return: dict{Node.id_, Node} - dict of nodes with nodes' id as a key
        """
        nodes: {Hashable, Node} = dict()
        read_data = data_input.load_data_from_file(path=path)
        for id_, prev_ids, duration in read_data[tuple(read_data.keys())[0]]:
            nodes[id_] = Node(id_, prev_ids.split(",") if prev_ids else [], float(duration))
        return nodes

    def show_result_network(self):
        pass

    def build(self):
        Window.clearcolor = (218/255, 222/255, 206/255, 1.0)

        sm = MyScreenManager()

        #nodes_by_id: {Hashable, Node} = self.load_data_from_user(path="cpm/test_data/111111 - straight path.txt")
        # nodes_by_id: {Hashable, Node} = self.load_data_from_user(path="cpm/test_data/131 - multiple possible networks (3).txt")
        # nodes_by_id: {Hashable, Node} = self.load_data_from_user(path="cpm/test_data/124 - 2 possible networks and 2 critical paths per network.txt")

        #nodes_by_id: {Hashable, Node} = self.load_data_from_lists(self.column_1_data,self.column_2_data,self.column_3_data)

        #networks: [Network, ] = Solver.solve(nodes_by_activity_id=nodes_by_id)

        return sm


CPMapp().run()