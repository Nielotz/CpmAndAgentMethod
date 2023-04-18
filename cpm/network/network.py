from typing import Self, Hashable, Callable

from cpm.node import Node, StartNode


class NetworkNode:
    """
    Double linked node with cpm.Node payload.

    id_ == node.activity.id_
    """

    def __init__(self, prev_network_nodes: [Self, ] = None, next_network_nodes: [Self, ] = None, node: Node = None):
        self.prev_network_nodes: [Self, ] = prev_network_nodes or []
        self.next_network_nodes: [Self, ] = next_network_nodes or []
        self.node: Node = node

    def __repr__(self):
        return f"prev: {[prev.id_ for prev in self.prev_network_nodes]}, " \
               f"next: {[next_.id_ for next_ in self.next_network_nodes]}, node: {self.node}"

    @property
    def id_(self):
        return self.node.activity.id_


class Network:
    """ Double linked network of nodes. """

    @property
    def critical_paths(self):
        if not self._critical_paths:
            self._critical_paths = self.calculate_critical_paths()

        return self._critical_paths

    @critical_paths.setter
    def critical_paths(self, critical_paths: [[Hashable, ], ]):
        self._critical_paths = critical_paths
    
    def __init__(self, nodes: {Hashable: Node}):
        """
        Create Network from nodes.

        @param nodes: {Node.id_: Node} - nodes from which create network
        """
        sorted_nodes = self._sorted(nodes)
        self.head: NetworkNode = NetworkNode(node=StartNode())
        # noinspection PyTypeChecker
        self.tail: NetworkNode = None

        self.network_node_by_activity_id: {Hashable: NetworkNode} = {}

        self._critical_paths: [[Hashable, ], ] = []

        for node_id, node in sorted_nodes.items():
            node: Node  # Add typing for PyCharm

            # When start node.
            if not node.activity.prev_activity:
                start_node: NetworkNode = NetworkNode(prev_network_nodes=[self.head, ], node=node)

                self.head.next_network_nodes.append(start_node)
                self.network_node_by_activity_id[node_id] = start_node
            else:
                # For each prev, set prev next and current prev.
                for prev_activity in node.activity.prev_activity:
                    prev_network_node: NetworkNode = self.network_node_by_activity_id[prev_activity]
                    curr_network_node: NetworkNode = NetworkNode(prev_network_nodes=[prev_network_node, ], node=node)

                    prev_network_node.next_network_nodes.append(curr_network_node)
                    self.network_node_by_activity_id[node_id] = curr_network_node

    def _sorted(self, nodes: {Hashable: Node}) -> {Hashable: Node}:
        """ Sorts nodes chronologically.

            Example:
                    |-H-I
                A-B-C-E-F-G
                  |-D
                May be sorted to:
                    ABCEFG D HI
                    ABC D EFG D HI
                    AB D CEFG  HI
                    AB C HI D EFG
                    etc.
                But never to:
                    D ABC...
                    A HI ...
        """
        to_parse: [Hashable, ] = list(nodes.keys())[::-1]
        parsed: {Hashable: Node} = {}  # Output dict.
        while to_parse:
            # Reverse order to allow to remove from list without changing positions of others.
            for node_id in to_parse[::-1]:
                node: Node = nodes[node_id]

                for prev_id in node.activity.prev_activity:
                    if prev_id in to_parse:
                        continue

                to_parse.remove(node_id)
                parsed[node_id] = node

        return parsed

    def calculate_critical_paths(self) -> [[Hashable, ], ]:
        """ Calculate critical paths. """

        is_critical: Callable[[NetworkNode], bool] = lambda network_node: not network_node.node.event.possible_delay

        critical_paths: [[Hashable, ], ] = []

        def find_req(node: NetworkNode, critical_path_: []):
            for network_node in node.next_network_nodes:
                if network_node.id_ == "FINISH":
                    critical_paths.append(critical_path_)
                elif is_critical(network_node):
                    find_req(network_node, critical_path_ + [network_node.id_])

        find_req(self.head, [])

        return critical_paths

    def print(self):
        def summarize_node(node: NetworkNode):
            return f"Prev: {[n.id_ for n in node.prev_network_nodes]}, " \
                   f"Next: {[n.id_ for n in node.next_network_nodes]}, " \
                   f"ID: {node.id_}, " \
                   f"ES: {node.node.event.early_start}, " \
                   f"EF: {node.node.event.early_final}, " \
                   f"LS: {node.node.event.late_start}, " \
                   f"LF: {node.node.event.late_final}, " \
                   f"Delay: {node.node.event.possible_delay}"

        def print_children_req(node: NetworkNode, prefix_size: int):
            prefix = '\t' * prefix_size
            print(f"{prefix}{summarize_node(node)}")
            for next_ in node.next_network_nodes:
                print_children_req(next_, prefix_size=prefix_size + 1)

        print(f"{summarize_node(self.head)}")
        for child in self.head.next_network_nodes:
            print_children_req(child, prefix_size=1)


