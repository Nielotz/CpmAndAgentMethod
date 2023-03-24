import pytest

import cpm.test.data_loader
from cpm.network import Network, Node


def test_straight_path():
    test_network: Network; expected_network: Network  # Type hinting for PyCharm
    test_network, expected_network = cpm.test.data_loader.load_data_from_file("cpm/test_data/straight_path.txt")
    test_network = test_network.solve()[0]

    # assert test_network.critical_paths == expected_network.critical_paths
    for test_node in test_network.nodes_by_id.values():
        for expected_node in expected_network.nodes_by_id.values():
            if expected_node.id_ == test_node.id_:
                # assert expected_node == test_node
                break
        else:
            pytest.fail("Node not found")

    for test_node in test_network.nodes_by_id.values():
        expected_node: Node = expected_network.nodes_by_id[test_node.id_]
        assert expected_node.early_start == test_node.early_start
        assert expected_node.early_final == test_node.early_final
        assert expected_node.late_start == test_node.late_start
        assert expected_node.late_final == test_node.late_final
        assert expected_node.possible_delay == test_node.possible_delay

def test_121_shorter_task():
    test_network: Network; expected_network: Network  # Type hinting for PyCharm
    test_network, expected_network = cpm.test.data_loader.load_data_from_file("cpm/test_data/121 - quick side task.txt")
    test_network = test_network.solve()[0]

    # assert test_network.critical_paths == expected_network.critical_paths
    for test_node in test_network.nodes_by_id.values():
        for expected_node in expected_network.nodes_by_id.values():
            if expected_node.id_ == test_node.id_:
                # assert expected_node == test_node
                break
        else:
            pytest.fail("Node not found")

    for test_node in test_network.nodes_by_id.values():
        expected_node: Node = expected_network.nodes_by_id[test_node.id_]
        assert expected_node.early_start == test_node.early_start
        assert expected_node.early_final == test_node.early_final
        assert expected_node.late_start == test_node.late_start
        assert expected_node.late_final == test_node.late_final
        assert expected_node.possible_delay == test_node.possible_delay
