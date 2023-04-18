from typing import Hashable

from kivy.app import App
from kivy.core.window import Window

import data_input
import gui.graph as graph
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

        nodes_by_id: {Hashable, Node} = self.load_data_from_user(path="cpm/test_data/12311 - 2 side orphans.txt")
        # nodes_by_id: {Hashable, Node} = self.load_data_from_user(path="cpm/test_data/131 - multiple possible networks (3).txt")
        # nodes_by_id: {Hashable, Node} = self.load_data_from_user(path="cpm/test_data/124 - 2 possible networks and 2 critical paths per network.txt")

        networks: [Network, ] = Solver.solve(nodes_by_activity_id=nodes_by_id)

        # gra = graph.GraphWidget()
        # gra.set_network(net[0])
        # gra.draw_graph(nn[0])
        return graph.GraphMeneger(net=networks, size=(5000,5000), size_hint=(None, None))

CPMapp().run()