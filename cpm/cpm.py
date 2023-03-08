# noinspection PyUnresolvedReferences
from cpm.network import Network


class CPM:
    def __init__(self):
        self.network: Network = Network()

    def load_data_from_user(self):
        """ Load data from user using UI. """
        pass

    def solve(self):
        self.network.solve()

    def print_result_network(self):
        pass

    def show_result_network(self):
        pass
