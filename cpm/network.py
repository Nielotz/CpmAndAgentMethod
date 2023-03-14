import copy
from typing import Hashable, Self
from kivy.logger import Logger

class Node:
    # noinspection PyTypeChecker
    def __init__(self, id_: str, prev_nodes: [Hashable, ], duration: float):
        """ A node in a CPM network. """

        """ Used to specify task to solve. """
        self.id_: str = id_  # Czynność
        self.prev_nodes: [Hashable, ] = copy.deepcopy(prev_nodes)
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

    def __init__(self, nodes_by_id: {Hashable, Node} = None):
        self.nodes_by_id: {Hashable, Node} = nodes_by_id or dict()
        self.critical_paths: [[Node, ], ] = []

    def add_node(self, node: Node):
        self.nodes_by_id[node.id_] = node

    def solve(self) -> [Self, ]:
        """
        Calculate missing nodes' params and critical path.

        Fix order.
        Traverse right.
        Fix orphan tasks.
        Traverse left.

        :return solved list of possible networks
        """

        """ Fix order. """
        def sort(network: Network):
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
            # Example ids: [0, 1, 2, 3]
            # Reverse order to allow to remove from list without changing others positions.
            nodes_ids_to_parse: [Hashable, ] = list(nodes.keys())[::-1]  # Example ids: [3, 2, 1, 0]
            parsed_nodes: {Node, } = dict()  # Output dict.
            while nodes_ids_to_parse:  # Iterate until there are nodes in wrong order.
                for node_id in nodes_ids_to_parse[::-1]:  # Return order to 0…N-1 to speed up in case of correct input.
                    node: Node = nodes[node_id]
                    if not node.prev_nodes:
                        node.early_start = node.late_start = node.possible_delay = 0  # Start
                    elif node.prev_nodes and None not in (
                            prev_early_first := [nodes[prev_id].early_final for prev_id in node.prev_nodes]):
                        node.early_start = max(prev_early_first)
                    else:
                        continue
                    node.early_final = node.early_start + node.duration
                    nodes_ids_to_parse.remove(node_id)
                    parsed_nodes[node.id_] = node

            return parsed_nodes


        """ Fix order and traverse right. """

        def sort_and_fill_es_and_ef(nodes: {Hashable: Node, }) -> {Hashable: Node, }:
            """
            Traverse events from start to end.

            Sorts nodes chronologically.
            Fills early_start and early_final.

            :return: dictionary of sorted nodes, mapped: {node.id_: Node}
            """
            # Example ids: [0, 1, 2, 3]
            # Reverse order to allow to remove from list without changing others positions.
            nodes_ids_to_parse: [Hashable, ] = list(nodes.keys())[::-1]  # Example ids: [3, 2, 1, 0]
            parsed_nodes: {Node, } = dict()  # Output dict.
            while nodes_ids_to_parse:  # Iterate until there are nodes in wrong order.
                for node_id in nodes_ids_to_parse[::-1]:  # Return order to 0…N-1 to speed up in case of correct input.
                    node: Node = nodes[node_id]
                    if not node.prev_nodes:
                        node.early_start = node.late_start = node.possible_delay = 0  # Start
                    elif node.prev_nodes and None not in (
                            prev_early_first := [nodes[prev_id].early_final for prev_id in node.prev_nodes]):
                        node.early_start = max(prev_early_first)
                    else:
                        continue
                    node.early_final = node.early_start + node.duration
                    nodes_ids_to_parse.remove(node_id)
                    parsed_nodes[node.id_] = node

            return parsed_nodes

        nodes: {Hashable: Node} = sort_and_fill_es_and_ef(dict(self.nodes_by_id))

        """ Fix orphan tasks. """

        def fix_orphan_tasks(nodes_sorted_start_to_final: {Hashable: Node, }) -> [{Hashable: Node}]:
            """
            Add missing prevs to make network end with one node.

            :return list of possible networks (eg. when 2 last tasks ends at the same time, both can be critical)
            """

            """ Filter all nodes without parent. """
            orphans_candidates: {Hashable: Node, } = dict(nodes_sorted_start_to_final)

            def pop_recursively_node_prevs_from_candidates(node: Node):
                for prev_node_id in node.prev_nodes:
                    if prev_node_id in orphans_candidates:
                        pop_recursively_node_prevs_from_candidates(orphans_candidates[prev_node_id])
                        orphans_candidates.pop(prev_node_id)

            _candidate_idx: int = 0
            while _candidate_idx < len(keys := tuple(orphans_candidates.keys())[::-1]):
                pop_recursively_node_prevs_from_candidates(nodes[keys[_candidate_idx]])
                _candidate_idx += 1


            """ Connect orphans, by making others prev to the final one. """

            Logger.info(f"Found {len(orphans_candidates)} orphans: {tuple(orphans_candidates.keys())}")

            candidate_final = {id_: node.early_start + node.duration for id_, node in orphans_candidates.items()}
            max_final_time: float = max(candidate_final.values())
            final_orphans = [id_ for id_, time in candidate_final.items() if time == max_final_time]

            possible_networks: [Network, ] = []
            for final_orphan in final_orphans:
                possible_networks.append(network := Network(nodes_by_id=copy.deepcopy(nodes_sorted_start_to_final)))
                for orphan in final_orphans:
                    if orphan != final_orphan:
                        network.nodes_by_id[final_orphan].prev_nodes.append(orphan)

            return possible_networks

        networks: [Network, ] = fix_orphan_tasks(nodes)
        Logger.info(f"Possible networks: {len(networks)}")

        for network in networks:
            network.nodes_by_id = sort_and_fill_es_and_ef(network.nodes_by_id)

        """ Traverse left. """

        #  Set last task and traverse backward: calculate: LS, LF, delay

        def traverse_backward(network_nodes: {Hashable: Node}):
            """
            Traverse events from final to the start.

            Fills late_start, late_final and possible_delay.
            """
            def fill_recursively_node_prevs(node: Node):
                for prev_node_id in node.prev_nodes:
                    prev_node: Node = network_nodes[prev_node_id]

                    prev_node.late_final = node.late_start
                    prev_node.late_start = prev_node.late_final - prev_node.duration
                    prev_node.possible_delay = prev_node.late_start - prev_node.early_start

                    fill_recursively_node_prevs(prev_node)

            # Fill final node values.
            last_node: Node = network_nodes[tuple(network_nodes.keys())[-1]]
            last_node.late_start = last_node.early_start
            last_node.late_final = last_node.early_final
            last_node.possible_delay = 0

            # Fill all other nodes.
            fill_recursively_node_prevs(last_node)

        for network in networks:
            traverse_backward(network.nodes_by_id)

        """ Get critical path, by selecting tasks with 0 possible delay. """
        # There can be multiple critical paths.
        # self.critical_paths = [[id1, id2...]]

        return networks

    def __repr__(self):
        return f"Network:\n" \
               f"\t Critical path:" + "\t\t".join([str(cp) for cp in self.critical_paths]) \
            + f"\n\tNodes: \n\t\t" + '\n\t\t'.join([str(node) for node in self.nodes])
