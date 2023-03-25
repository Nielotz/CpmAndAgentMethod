import copy
from typing import Hashable, Self
from kivy.logger import Logger


class Activity:
    def __init__(self, id_: str, prev_activity: [Hashable, ], duration: float):
        self.id_: str = id_
        self.prev_activity: [Hashable, ] = copy.deepcopy(prev_activity)
        self.duration: float = duration

        # noinspection PyTypeChecker
        self.start_event: Event = None
        # noinspection PyTypeChecker
        self.finish_event: Event = None

class Event:
    early_start: float = None
    early_final: float = None
    late_start: float = None
    late_final: float = None
    possible_delay: float = None


class Node:
    def __init__(self, id_: str, prev_activity: [Hashable, ], duration: float):
        """
        A node in a CPM network.

        Contains activity + activity end event.
        """

        self.activity: Activity = Activity(id_=id_, prev_activity=prev_activity, duration=duration)
        self.event: Event = Event()

    def asdict(self):
        return {
            "id_": self.activity.id_, "prev_nodes": self.activity.prev_activity, "duration": self.activity.duration,
            "early_start": self.event.early_start, "early_final": self.event.early_final,
            "late_start": self.event.late_start, "late_final": self.event.late_final,
            "possible_delay": self.event.possible_delay
        }

    def __repr__(self):
        return str(self.asdict())


class Network:
    """ Holds Nodes and calculates CPM method params. """

    def __init__(self, nodes_by_activity_id: {Hashable, Node} = None):
        self.nodes_by_activity_id: {Hashable, Node} = nodes_by_activity_id or dict()
        self.critical_paths: [[Node, ], ] = []

    def add_node(self, node: Node):
        self.nodes_by_activity_id[node.activity.id_] = node

    def _sorted(self) -> Self:
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
        nodes = self.nodes_by_activity_id

        to_parse: [Hashable, ] = list(nodes.keys())[::-1]
        parsed: Network = Network()  # Output dict.
        while to_parse:
            # Reverse order to allow to remove from list without changing positions of others.
            for node_id in to_parse[::-1]:
                node: Node = nodes[node_id]

                for prev_id in node.activity.prev_activity:
                    if prev_id in to_parse:
                        continue

                to_parse.remove(node_id)
                parsed.add_node(node)

        return parsed

    def fill_es_and_ef(self):
        """
        Traverse events forward - from start to end.

        Fills early_start and early_final.

        Requires sorted nodes that no prev is on right of any node.
        """
        for node in self.nodes_by_activity_id.values():
            if not node.activity.prev_activity:  # Start
                node.event.early_start = node.event.late_start = node.possible_delay = 0
            else:
                node.event.early_start = max([self.nodes_by_activity_id[prev_id].early_final for prev_id in node.activity.prev_activity])

            node.early_final = node.event.early_start + node.activity.duration

    def solve(self) -> [Self, ]:
        """
        Calculate missing nodes' params and critical path.

        Fix order.
        Traverse right.
        Fix orphan tasks.
        Traverse left.

        :return solved list of possible networks
        """
        self.nodes_by_activity_id = self._sorted().nodes_by_activity_id

        self.fill_es_and_ef()

        """ Fix orphan tasks. """

        def fix_orphan_tasks(nodes_sorted_start_to_final: {Hashable: Node, }) -> [{Hashable: Node}]:
            """
            Add missing prevs to make network end with one node.

            :return list of possible networks (eg. when 2 last tasks ends at the same time, both can be critical)
            """

            """ Filter all nodes without parent. """
            orphans_candidates: {Hashable: Node, } = dict(nodes_sorted_start_to_final)

            def pop_recursively_node_prevs_from_candidates(node: Node):
                for prev_node_id in node.activity.prev_activity:
                    if prev_node_id in orphans_candidates:
                        pop_recursively_node_prevs_from_candidates(orphans_candidates[prev_node_id])
                        orphans_candidates.pop(prev_node_id)

            _candidate_idx: int = 0
            while _candidate_idx < len(keys := tuple(orphans_candidates.keys())[::-1]):
                pop_recursively_node_prevs_from_candidates(self.nodes_by_activity_id[keys[_candidate_idx]])
                _candidate_idx += 1


            """ Connect orphans, by making others prev to the final one. """

            Logger.info(f"Found {len(orphans_candidates)} orphans: {tuple(orphans_candidates.keys())}")

            candidate_final = {id_: node.event.early_start + node.activity.duration for id_, node in orphans_candidates.items()}
            max_final_time: float = max(candidate_final.values())
            final_orphans = [id_ for id_, time in candidate_final.items() if time == max_final_time]

            possible_networks: [Network, ] = []
            for final_orphan in final_orphans:
                possible_networks.append(network := Network(nodes_by_activity_id=copy.deepcopy(nodes_sorted_start_to_final)))
                for orphan in candidate_final:
                    if orphan != final_orphan:
                        network.nodes_by_activity_id[final_orphan].activity.prev_activity.append(orphan)

            return possible_networks

        networks: [Network, ] = fix_orphan_tasks(self.nodes_by_activity_id)
        Logger.info(f"Possible networks: {len(networks)}")

        # for network in networks:
        #     network.nodes_by_id = fill_es_and_ef(network.nodes_by_id)

        """ Traverse left. """

        #  Set last task and traverse backward: calculate: LS, LF, delay

        def traverse_backward(network_nodes: {Hashable: Node}):
            """
            Traverse events from final to the start.

            Fills late_start, late_final and possible_delay.
            """
            def fill_recursively_node_prevs(node: Node):
                for prev_node_id in node.activity.prev_activity:
                    prev_node: Node = network_nodes[prev_node_id]

                    prev_node.late_final = node.event.late_start
                    prev_node.event.late_start = prev_node.late_final - prev_node.activity.duration
                    prev_node.possible_delay = prev_node.event.late_start - prev_node.event.early_start

                    fill_recursively_node_prevs(prev_node)

            # Fill final node values.
            last_node: Node = network_nodes[tuple(network_nodes.keys())[-1]]
            last_node.event.late_start = last_node.event.early_start
            last_node.late_final = last_node.event.early_final
            last_node.possible_delay = 0

            # Fill all other nodes.
            fill_recursively_node_prevs(last_node)

        for network in networks:
            traverse_backward(network.nodes_by_activity_id)

        """ Get critical path, by selecting tasks with 0 possible delay. """
        # There can be multiple critical paths.
        # self.critical_paths = [[id1, id2...]]

        return networks

    def __repr__(self):
        return f"Network:\n" \
               f"\t Critical path:" + "\t\t".join([str(cp) for cp in self.critical_paths]) \
            + f"\n\tNodes: \n\t\t" + '\n\t\t'.join([str(node) for node in self.nodes_by_activity_id.values()])
