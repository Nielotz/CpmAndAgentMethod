import copy
from typing import Hashable, Self

from kivy.logger import Logger

from cpm.network.network import NetworkNode, Network
from cpm.node import Node, ApparentNode, FinalNode


class Solver:
    """ Holds Nodes and calculates CPM method params. """

    def _fill_es_and_ef(self, head: NetworkNode):
        """
        Traverse events forward - from start to end.

        Fills early_start and early_final.
        """

        def fill_es_and_ef_req(start_node: NetworkNode):
            node: Node = start_node.node

            prev_early_finals = [prev.node.event.early_final for prev in start_node.prev_network_nodes]

            # When there is another branch not yet filled.
            if None in prev_early_finals:
                return

            local_early_start = max(prev_early_finals)

            # When branch delays early start.
            # if node.event.early_start is None or node.event.early_start < local_early_start:
            node.event.early_start = local_early_start
            node.event.early_final = local_early_start + node.activity.duration

            for next_node in start_node.next_network_nodes:
                fill_es_and_ef_req(next_node)

        for network_node in head.next_network_nodes:
            fill_es_and_ef_req(network_node)

    def _add_apparent_activity_between_orphan_nodes(self, network: Network) -> [Network]:
        """
        Fix orphan tasks.

        When there are multiple critical paths, there may be multiple possible networks.

        Adds final dummy node at the end.
        """
        orphans: [NetworkNode] = []

        def find_orphan_nodes_req(network_node: NetworkNode):
            if not network_node.next_network_nodes:
                orphans.append(network_node)
            else:
                for next_node in network_node.next_network_nodes:
                    find_orphan_nodes_req(next_node)

        find_orphan_nodes_req(network.head)

        early_finals = [(network_node.node.event.early_final, network_node) for network_node in orphans]
        final_time = max(early_finals)[0]
        last_nodes: [NetworkNode] = [node_ for early_final, node_ in early_finals if early_final == final_time]

        possible_networks: [Network] = []

        for last_node in last_nodes:
            last_node: NetworkNode

            network_: Network = copy.deepcopy(network)
            possible_networks.append(network_)

            last_node_: NetworkNode = network_.network_node_by_activity_id[last_node.id_]

            # Dummy node past tree.
            finish_node_: NetworkNode = NetworkNode(node=FinalNode(last_node_.node.event),
                                                    prev_network_nodes=[last_node_])
            last_node_.next_network_nodes.append(finish_node_)

            network_.tail = finish_node_

            orphans_: [NetworkNode, ] = orphans[:]
            orphans_.remove(last_node)
            for orphan in orphans_:
                # Add apparent task that connects orphans to the last_node.
                orphan_: NetworkNode = network_.network_node_by_activity_id[orphan.id_]

                # Connect orphan to last_node.
                apparent_network_node: NetworkNode = NetworkNode(next_network_nodes=[last_node_],
                                                               prev_network_nodes=[orphan_],
                                                               node=ApparentNode(
                                                               activity_name=f"apparent_{orphan_.id_}->{last_node_.id_}",
                                                               event=last_node_.node.event))
                last_node_.prev_network_nodes.append(apparent_network_node)
                orphan_.next_network_nodes.append(apparent_network_node)

        return possible_networks

    def _fill_ls_lf_and_delay(self, tail: NetworkNode):
        """
        Traverse events from final to the start.

        Fills late_start, late_final and possible_delay.
        """

        def fill_ls_lf_and_delay_req(start_node: NetworkNode):
            # Welp, something needs to be done here.
            if "apparent" not in start_node.id_:
                node: Node = start_node.node

                if len(start_node.next_network_nodes) == 1 and "apparent" in start_node.next_network_nodes[0].id_:
                    next_late_starts = [next_node.node.event.late_final for next_node in start_node.next_network_nodes]
                else:
                    next_late_starts = [next_node.node.event.late_start for next_node in start_node.next_network_nodes]

                # Other branch needs to be filled first.
                if None in next_late_starts:
                    return

                node.event.late_final = min(next_late_starts)
                node.event.late_start = node.event.late_final - node.activity.duration
                node.event.possible_delay = node.event.late_start - node.event.early_start

            for prev_node in start_node.prev_network_nodes:
                fill_ls_lf_and_delay_req(prev_node)

        # Fill final node values.
        last_event = tail.node.event
        last_event.late_start = last_event.early_start = last_event.late_final = last_event.early_final
        last_event.possible_delay = 0

        # Fill all other nodes.
        for prev_node in tail.prev_network_nodes:
            fill_ls_lf_and_delay_req(prev_node)

    def solve(self, nodes_by_activity_id: {Hashable, Node} = None) -> [Self, ]:
        """
        Organize tasks, create network, add apparent tasks, solve: missing nodes' params and critical path.

        Build network.
        Traverse right - fill es and ef.
        Fix orphan tasks.
        Traverse left - fill ls, lf and delay.
        Calculate critical paths.

        @return: solved list of possible networks
        """

        """ Fix order and build network. """
        network: Network = Network(nodes=nodes_by_activity_id)

        """ Traverse right. """
        self._fill_es_and_ef(network.head)

        """ Fix orphan tasks. """
        networks: [Network, ] = self._add_apparent_activity_between_orphan_nodes(network=network)

        Logger.info(f"Solve: Possible networks: {len(networks)}")

        """ Traverse left. """
        for network in networks:
            self._fill_ls_lf_and_delay(network.tail)

        """ Get critical path, by selecting tasks with 0 possible delay. """
        for network_idx, network in enumerate(networks):
            network.calculate_critical_paths()
            Logger.info(f"Solve: Network {network_idx + 1}: "
                        f"found {len(network.critical_paths)} critical paths: {network.critical_paths}")

        return networks

    # def __repr__(self):
    #     return f"Network:\n\tNodes: \n\t\t" + '\n\t\t'.join([str(node) for node in self._nodes_by_activity_id.values()])
        # f"\t Critical path:" + "\t\t".join([str(cp) for cp in self.critical_paths])
