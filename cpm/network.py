import copy
from typing import Self, NamedTuple


class Node:
    def __init__(self, id_: str, prev_nodes: [Self, ], duration: float,
                 early_start: float = 0, early_final: float = 0, late_start: float = 0, late_final: float = 0,
                 possible_delay: float = 0):
        """ A node in a CPM network. """

        """ Used to specify task to solve. """
        self.id_: str = id_  # Czynność
        self.prev_nodes: [Self, ] = copy.deepcopy(prev_nodes)
        self.duration: float = duration

        """ Calculated using Network.solve """
        self.early_start: float = early_start
        self.early_final: float = early_final
        self.late_start: float = late_start
        self.late_final: float = late_final
        self.possible_delay: float = possible_delay

    def __repr__(self):
        return f"id_: {self.id_}, prev_nodes: {self.prev_nodes}, duration: {self.duration}, " \
               f"early_start: {self.early_start}, early_final: {self.early_final}, " \
               f"late_start: {self.late_start}, late_final: {self.late_final}, possible_delay: {self.possible_delay}"

class Network:
    """ Holds Nodes and calculates CPM method params. """
    nodes: [Node, ] = []
    critical_paths: [[Node, ], ] = []

    def add_node(self, node: Node):
        self.nodes.append(node)

    def solve(self):
        """ Calculate missing nodes' params and critical path. """

        # There can be multiple critical paths.
        # self.critical_paths = [[id1, id2...]]
        pass

    def __repr__(self):
        return f"Network:\n" \
               f"\t Critical path:" + "\t\t".join(self.critical_paths) \
        + f"\n\tNodes: \n \t\t" + '\t\t'.join([str(node) for node in self.nodes])
