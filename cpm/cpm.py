from typing import Hashable

import data_input
from cpm.network.network import Network
from cpm.node import Node
from cpm.solver import Solver


class CPM:
    def __init__(self):
        self.network_data: {Hashable, Node} = None
        self.result_networks: [Network, ] = None
    def load_data_from_user(self, path: str):
        read_data = data_input.load_data_from_file(path=path)
        for id_, prev_ids, duration in read_data[read_data.keys()[0]]:
            self.network_data[id_] = Node(id_, prev_ids.split(",") if prev_ids else [], float(duration))

    def solve(self):
        self.result_networks = Solver(nodes_by_activity_id=self.network_data).solve()
        # self.result_networks = Solver.solve(nodes_by_activity_id=self.network_data)

    def print_result_network(self):
        pass

    def show_result_network(self):
        pass
