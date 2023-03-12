import data_input
from cpm.network import Network, Node


def load_data_from_file(path: str = "cpm/test_data/simple_test.txt", sep: str = ";") -> [Network, Network]:
    """
    Load test data from file.

    :return test network, expected network
    """
    test_network: Network = Network()
    expected_network: Network = Network()

    read_data = data_input.load_data_from_file(path=path, sep=sep)

    # for data
    for header, data in read_data.items():
        if header == "STHUNIQUE DATA":
            for id_, prev_ids, duration in data:
                test_network.add_node(Node(id_, prev_ids.split(",") if prev_ids else [], float(duration)))
        elif header == "STHUNIQUE RESULTS":
            expected_network.critical_paths = data[0]
            expected_network.nodes = []
            # Czynność;ES;                 EF;         LS;         LF;Rezerwa
            for id_, early_start, early_final, late_start, late_final, delay in data[1:]:
                node = Node(id_, [], 0)
                node.early_start = float(early_start)
                node.early_final = float(early_final)
                node.late_start = float(late_start)
                node.late_final = float(late_final)
                node.possible_delay = float(delay)

                expected_network.add_node(node)

    return test_network, expected_network
