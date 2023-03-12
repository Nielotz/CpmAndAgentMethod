import copy
from typing import Any


class Node:
    # noinspection PyTypeChecker
    def __init__(self, id_: str, prev_nodes: [Any, ], duration: float):
        """ A node in a CPM network. """

        """ Used to specify task to solve. """
        self.id_: str = id_  # Czynność
        self.prev_nodes: [Any, ] = copy.deepcopy(prev_nodes)
        self.duration: float = duration

        """ Calculated using Network.solve """
        self.early_start: float = None
        self.early_final: float = None
        self.late_start: float = None
        self.late_final: float = None
        self.possible_delay: float = None

    def asdict(self):
        return {
            "id_": self.id_, "prev_nodes": self.prev_nodes, "duration": self.duration,
            "early_start": self.early_start, "early_final": self.early_final,
            "late_start": self.late_start, "late_final": self.late_final,
            "possible_delay": self.possible_delay
        }

    def __repr__(self):
        return str(self.asdict())


class Network:
    """ Holds Nodes and calculates CPM method params. """
    nodes: [Node, ] = []
    nodes_by_id: {} = dict()
    critical_paths: [[Node, ], ] = []

    def add_node(self, node: Node):
        self.nodes.append(node)
        self.nodes_by_id[node.id_] = node

    def solve(self):
        """ Calculate missing nodes' params and critical path. """

        # Traverse to the end: calculate: ES, EF
        def traverse_to_right():
            """
            Traverse events from start to the end.

            Fills early_start and early_final.

            :return: list somehow sorted: from the last to the first. First item is always the final one.
            """
            nodes_to_parse: [int, ] = list(range(len(self.nodes)))[::-1]
            parsed_nodes: [Node, ] = []
            while len(nodes_to_parse) > 0:
                for node_id in nodes_to_parse[::-1]:
                    node: Node = self.nodes[node_id]
                    if not node.prev_nodes:
                        node.early_start = node.late_start = node.possible_delay = 0  # Start
                        node.early_final = node.early_start + node.duration
                    elif node.prev_nodes and None not in (
                            prev_early_first := [self.nodes_by_id[prev_id].early_final for prev_id in node.prev_nodes]):
                        node.early_start = max(prev_early_first)
                        node.early_final = node.early_start + node.duration
                    else:
                        continue
                    nodes_to_parse.remove(node_id)
                    parsed_nodes.append(node)

            return parsed_nodes

        pre_sorted: [Node] = traverse_to_right()

        # Traverse backward: calculate: LS, LF, delay
        def traverse_backward(nodes: [Node]):
            """
            Traverse events from end to the start.

            Fills late_start, late_final and possible_delay.
            """

        traverse_backward(pre_sorted)
        # self.late_start: float = late_start
        # self.late_final: float = late_final
        # self.possible_delay: float = possible_delay

        """ Fix orphan tasks. """
        # Add apparent tasks that connect to the final one.

        """ Get critical path, by selecting tasks with 0 possible delay. """
        # There can be multiple critical paths.
        # self.critical_paths = [[id1, id2...]]
        pass

    def __repr__(self):
        return f"Network:\n" \
               f"\t Critical path:" + "\t\t".join([str(cp) for cp in self.critical_paths]) \
            + f"\n\tNodes: \n\t\t" + '\n\t\t'.join([str(node) for node in self.nodes])
