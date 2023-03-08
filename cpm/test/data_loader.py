import data_input
from cpm.network import Network, Node


def load_data_from_file(path: str = "cpm/test_data/simple_test.txt", sep: str = ";") -> [Network, Network]:
    """
    Load test data from file.

    :return test network, result network
    """
    test_network: Network = Network()
    expected_network: Network = Network()

    read_data = data_input.load_data_from_file(path=path, sep=sep)

    # for data
    for header, data in read_data.items():
        if header == "STHUNIQUE DATA":
            test_network.nodes = [Node(id_, prev_ids.split(","), float(duration)) for id_, prev_ids, duration in data]
        elif header == "STHUNIQUE RESULTS":
            expected_network.critical_paths = data[0]
            expected_network.nodes = [
                Node(id_, prev_ids.split(","), duration, early_start, early_final, late_start, late_final, delay)
                for id_, prev_ids, duration, early_start, early_final, late_start, late_final, delay in data[1:]]

    return test_network, expected_network