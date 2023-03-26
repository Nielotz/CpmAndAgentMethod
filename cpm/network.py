import copy
from typing import Hashable, Self

from kivy.logger import Logger


class Activity:
    def __init__(self, id_: str, prev_activity_id: [Hashable, ], duration: float):
        self.id_: str = id_
        self.prev_activity: [Hashable, ] = copy.deepcopy(prev_activity_id)
        self.duration: float = duration


class Event:
    def __init__(self, early_start: float = None, early_final: float = None,
                 late_start: float = None, late_final: float = None,
                 possible_delay: float = None):
        self.early_start: float = early_start
        self.early_final: float = early_final
        self.late_start: float = late_start
        self.late_final: float = late_final
        self.possible_delay: float = possible_delay


class Node:
    def __init__(self, activity_id_: str, prev_activity_id: [Hashable, ], duration: float):
        """
        A node in a CPM network.

        Contains activity + activity end event.
        """

        self.activity: Activity = Activity(id_=activity_id_, prev_activity_id=prev_activity_id, duration=duration)
        self.event: Event = Event()

    def asdict(self):
        return {
            "id_": self.activity.id_, "prev_activity": self.activity.prev_activity, "duration": self.activity.duration,
            "early_start": self.event.early_start, "early_final": self.event.early_final,
            "late_start": self.event.late_start, "late_final": self.event.late_final,
            "possible_delay": self.event.possible_delay
        }

    def __repr__(self):
        return str(self.asdict())


class ApparentNode(Node):
    """ No activity, zeroed event. """

    # noinspection PyMissingConstructor
    def __init__(self, activity_name="apparent", event: Event = None):
        self.activity = Activity(activity_name, [], 0)
        self.event = event or Event(0, 0, 0, 0, 0)


class StartNode(ApparentNode):
    """ No activity, zeroed event. """

    # noinspection PyMissingConstructor
    def __init__(self):
        super().__init__(activity_name="START")


class FinalNode(ApparentNode):
    """ No activity. """

    # noinspection PyMissingConstructor
    def __init__(self, last_event: Event):
        super().__init__(activity_name="FINISH", event=copy.deepcopy(last_event))
        self.event.early_start = self.event.late_start = self.event.late_final = self.event.early_final
        self.event.possible_delay = 0


class Network:
    """ Holds Nodes and calculates CPM method params. """

    class Graph:
        class GraphNode:
            def __init__(self, prev_graph_nodes: [Self, ] = None, next_graph_nodes: [Self, ] = None, node: Node = None):
                self.prev_graph_nodes: [Self, ] = prev_graph_nodes or []
                self.next_graph_nodes: [Self, ] = next_graph_nodes or []
                self.node = node

            def __repr__(self):
                return f"prev: {[prev.id_ for prev in self.prev_graph_nodes]}, " \
                       f"next: {[next.id_ for next in self.next_graph_nodes]}, node: {self.node}"

            @property
            def id_(self):
                return self.node.activity.id_

        def print(self):
            def get_id(node: Network.Graph.GraphNode):
                return node.node.activity.id_

            def summarize_node(node: Network.Graph.GraphNode):
                return f"Prev: {[n.id_ for n in node.prev_graph_nodes]}, " \
                       f"Next: {[n.id_ for n in node.next_graph_nodes]}, " \
                       f"ID: {node.id_}, " \
                       f"ES: {node.node.event.early_start}, " \
                       f"EF: {node.node.event.early_final}, " \
                       f"LS: {node.node.event.late_start}, " \
                       f"LF: {node.node.event.late_final}, " \
                       f"Delay: {node.node.event.possible_delay}"

            def print_children_req(node: Network.Graph.GraphNode, prefix_size: int):
                prefix = '\t' * prefix_size
                print(f"{prefix}{summarize_node(node)}")
                for next_ in node.next_graph_nodes:
                    print_children_req(next_, prefix_size=prefix_size + 1)

            print(f"{summarize_node(self.head)}")
            for child in self.head.next_graph_nodes:
                print_children_req(child, prefix_size=1)

        def __init__(self, sorted_network: "Network"):
            """
            @param sorted_network: nodes to create graph from, provided chronologically - parent, child
            """
            # noinspection PyPep8Naming
            GraphNode = Network.Graph.GraphNode
            self.head: GraphNode = GraphNode(node=StartNode())
            # noinspection PyTypeChecker
            self.tail: GraphNode = None
            self.graph_node_by_activity_id: {Hashable: GraphNode} = {}

            for node_id, node in sorted_network.nodes_by_activity_id.items():
                node: Node  # Fix PyCharm typing
                # When start node.
                if not node.activity.prev_activity:
                    start_node: GraphNode = GraphNode(prev_graph_nodes=[self.head, ], node=node)

                    self.head.next_graph_nodes.append(start_node)
                    self.graph_node_by_activity_id[node_id] = start_node
                else:
                    # For each prev, set prev next and current prev.
                    for prev_activity in node.activity.prev_activity:
                        prev_graph_node: GraphNode = self.graph_node_by_activity_id[prev_activity]
                        curr_graph_node: GraphNode = GraphNode(prev_graph_nodes=[prev_graph_node, ], node=node)

                        prev_graph_node.next_graph_nodes.append(curr_graph_node)
                        self.graph_node_by_activity_id[node_id] = curr_graph_node

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

    def build_graph(self):
        return Network.Graph(self._sorted())

    def fill_es_and_ef(self, head: Graph.GraphNode):
        """
        Traverse events forward - from start to end.

        Fills early_start and early_final.
        """

        def fill_es_and_ef_req(start_node: Network.Graph.GraphNode):
            node: Node = start_node.node

            prev_early_finals = [prev.node.event.early_final for prev in start_node.prev_graph_nodes]

            # When there is another branch not yet filled.
            if None in prev_early_finals:
                return

            local_early_start = max(prev_early_finals)

            # When branch delays early start.
            # if node.event.early_start is None or node.event.early_start < local_early_start:
            node.event.early_start = local_early_start
            node.event.early_final = local_early_start + node.activity.duration

            for next_node in start_node.next_graph_nodes:
                fill_es_and_ef_req(next_node)

        for graph_node in head.next_graph_nodes:
            fill_es_and_ef_req(graph_node)

    def add_apparent_activity_between_orphan_nodes(self, graph: Graph) -> [Graph]:
        """
        Fix orphan tasks.

        When there are multiple critical paths, there may be multiple possible graphs.

        Adds final dummy node at the end.
        """
        # noinspection PyPep8Naming
        GraphNode = Network.Graph.GraphNode

        orphans: [GraphNode] = []

        def find_orphan_nodes_req(graph_node: GraphNode):
            if not graph_node.next_graph_nodes:
                orphans.append(graph_node)
            else:
                for next_node in graph_node.next_graph_nodes:
                    find_orphan_nodes_req(next_node)

        find_orphan_nodes_req(graph.head)

        early_finals = [(graph_node.node.event.early_final, graph_node) for graph_node in orphans]
        final_time = max(early_finals)[0]
        last_nodes: [GraphNode] = [graph_node for early_final, graph_node in early_finals if early_final == final_time]

        possible_graphs: [Network.Graph] = []

        for last_node in last_nodes:
            last_node: GraphNode

            graph_: Network.Graph = copy.deepcopy(graph)
            possible_graphs.append(graph_)

            last_node_: GraphNode = graph_.graph_node_by_activity_id[last_node.id_]

            # Dummy node past tree.
            finish_node_: GraphNode = GraphNode(node=FinalNode(last_node_.node.event), prev_graph_nodes=[last_node_])
            last_node_.next_graph_nodes.append(finish_node_)

            graph_.tail = finish_node_

            orphans_: [GraphNode, ] = orphans[:]
            orphans_.remove(last_node)
            for orphan in orphans_:
                # Add apparent task that connects orphans to the last_node.
                orphan_: GraphNode = graph_.graph_node_by_activity_id[orphan.id_]

                # Connect orphan to last_node.
                apparent_graph_node: GraphNode = GraphNode(next_graph_nodes=[last_node_],
                                                           prev_graph_nodes=[orphan_],
                                                           node=ApparentNode(
                                                               activity_name=f"apparent_{orphan_.id_}->{last_node_.id_}",
                                                               event=last_node_.node.event))
                last_node_.prev_graph_nodes.append(apparent_graph_node)
                orphan_.next_graph_nodes.append(apparent_graph_node)

        return possible_graphs

    def fill_ls_lf_and_delay(self, tail: Graph.GraphNode):
        """
        Traverse events from final to the start.

        Fills late_start, late_final and possible_delay.
        """
        def fill_ls_lf_and_delay_req(start_node: Network.Graph.GraphNode):
            # Welp, something needs to be done here.
            if "apparent" not in start_node.id_:
                node: Node = start_node.node

                if len(start_node.next_graph_nodes) == 1 and "apparent" in start_node.next_graph_nodes[0].id_:
                    next_late_starts = [next_node.node.event.late_final for next_node in start_node.next_graph_nodes]
                else:
                    next_late_starts = [next_node.node.event.late_start for next_node in start_node.next_graph_nodes]

                # Other branch needs to be filled first.
                if None in next_late_starts:
                    return

                node.event.late_final = min(next_late_starts)
                node.event.late_start = node.event.late_final - node.activity.duration
                node.event.possible_delay = node.event.late_start - node.event.early_start

            for prev_node in start_node.prev_graph_nodes:
                fill_ls_lf_and_delay_req(prev_node)

        # Fill final node values.
        last_event = tail.node.event
        last_event.late_start = last_event.early_start = last_event.late_final = last_event.early_final
        last_event.possible_delay = 0

        # Fill all other nodes.
        for prev_node in tail.prev_graph_nodes:
            fill_ls_lf_and_delay_req(prev_node)

    def solve(self) -> [Self, ]:
        """
        Calculate missing nodes' params and critical path.

        Fix order.
        Traverse right.
        Fix orphan tasks.
        Traverse left.

        @return solved list of possible networks
        """

        """ Fix order and build graph. """
        graph: Network.Graph = self.build_graph()

        """ Traverse right. """
        self.fill_es_and_ef(graph.head)

        """ Fix orphan tasks. """
        graphs: [Network.Graph, ] = self.add_apparent_activity_between_orphan_nodes(graph=graph)
        Logger.info(f"Possible graphs: {len(graphs)}")

        graph = graphs[0]

        """ Traverse left. """
        # Find last node.
        self.fill_ls_lf_and_delay(graph.tail)

        # for network in networks:
        #     traverse_backward(network.nodes_by_activity_id)

        """ Get critical path, by selecting tasks with 0 possible delay. """
        # There can be multiple critical paths.
        # self.critical_paths = [[id1, id2...]]

        self.nodes_by_activity_id = graph.graph_node_by_activity_id
        return graphs

    def __repr__(self):
        return f"Network:\n" \
               f"\t Critical path:" + "\t\t".join([str(cp) for cp in self.critical_paths]) \
            + f"\n\tNodes: \n\t\t" + '\n\t\t'.join([str(node) for node in self.nodes_by_activity_id.values()])
