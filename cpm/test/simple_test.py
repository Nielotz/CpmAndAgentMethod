import pytest

import cpm.test.data_loader
from cpm.network import Network, Node


def runner(path: str):
    test_network: Network; expected_network: Network  # Type hinting for PyCharm
    test_network, expected_network = cpm.test.data_loader.load_data_from_file("cpm/test_data/111111 - straight path.txt")
    result_graph: Network.Graph = test_network.solve()[0]

    result_nodes = [graph_node.node for graph_node in result_graph.graph_node_by_activity_id.values()]
    expected_nodes = tuple(expected_network.nodes_by_activity_id.values())

    # assert test_network.critical_paths == expected_graph.critical_paths
    for test_node in result_nodes:
        for expected_node in expected_nodes:
            if expected_node.activity.id_ == test_node.activity.id_:
                # assert expected_node == test_node
                break
        else:
            pytest.fail("Node not found")

    for test_node in result_nodes:
        expected_node: Node =  expected_network.nodes_by_activity_id[test_node.activity.id_]
        assert expected_node.event.early_start == test_node.event.early_start
        assert expected_node.event.early_final == test_node.event.early_final
        assert expected_node.event.late_start == test_node.event.late_start
        assert expected_node.event.late_final == test_node.event.late_final
        assert expected_node.event.possible_delay == test_node.event.possible_delay

def test_straight_path():
    runner("cpm/test_data/111111 - straight path.txt")

def test_121_shorter_task():
    runner("cpm/test_data/121 - quick side task.txt")

def test_112_two_orphans():
    runner("cpm/test_data/112 - two orphans.txt")