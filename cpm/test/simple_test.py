import pytest

import cpm.test.data_loader
from cpm.network import Network


def test_simple():
    test_network: Network; result_network: Network  # Type hinting for PyCharm
    test_network, result_network = cpm.test.data_loader.load_data_from_file()
    test_network.solve()

    assert test_network.critical_paths == result_network.critical_paths
    for test_node in test_network.nodes:
        for expected_node in result_network.nodes:
            if expected_node.id_ == test_node.id_:
                assert expected_node == test_node
                break
        else:
            pytest.fail("Node not found")
