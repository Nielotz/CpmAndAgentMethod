from typing import Hashable

import data_input
from cpm.network.network import Network
from cpm.node import Node, Event


def load_data_from_file(path: str = "cpm/test_data/111111 - straight path.txt", sep: str = ";") \
        -> [{Hashable, Node}, Network]:
    """
    Load test data from file.

    @return test network, expected network
    """
    test_network_nodes: {Hashable, Node} = {}
    expected_network_nodes: {Hashable, Node} = {}
    expected_network_critical_paths: [[]] = []

    read_data = data_input.load_data_from_file(path=path, sep=sep)

    for header, data in read_data.items():
        if header == "STHUNIQUE DATA":
            for id_, prev_ids, duration in data:
                test_network_nodes[id_] = Node(id_, prev_ids.split(",") if prev_ids else [], float(duration))
        elif header == "STHUNIQUE RESULTS":
            expected_network_critical_paths = data[0]
            # Czynność;ES;                 EF;         LS;         LF;Rezerwa
            for id_, early_start, early_final, late_start, late_final, delay in data[1:]:
                event: Event = Event(early_start=float(early_start), early_final=float(early_final),
                                     late_start=float(late_start), late_final=float(late_final),
                                     possible_delay=float(delay))

                expected_network_nodes[id_] = Node(id_, [], 0, event=event)
    expected_network = Network(expected_network_nodes)
    expected_network.critical_paths = expected_network_critical_paths
    return test_network_nodes, expected_network
