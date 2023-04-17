from typing import Hashable

import pytest

import cpm.test.data_loader
from cpm.network.network import Network, NetworkNode
from cpm.solver import Solver
from cpm.node import Node


def runner(path: str):
    test_network_data: {Hashable, Node}; expected_network: Network  # Type hinting for PyCharm
    test_network_data, expected_network = cpm.test.data_loader.load_data_from_file(path)

    result_network: Network = Solver().solve(nodes_by_activity_id=test_network_data)[0]

    result_nodes: [Node, ] = [network_node.node for network_node in result_network.network_node_by_activity_id.values()]
    expected_nodes: [Node, ] = [node_.node for node_ in tuple(expected_network.network_node_by_activity_id.values())]


    # assert test_network.critical_paths == expected_network.critical_paths
    for test_node in result_nodes:
        for expected_node in expected_nodes:
            if expected_node.activity.id_ == test_node.activity.id_:
                # assert expected_node == test_node
                break
        else:
            pytest.fail("Node not found")

    for test_node in result_nodes:
        expected_node: Node =  expected_network.network_node_by_activity_id[test_node.activity.id_].node
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

# def test_one_critical_path():
#     runner("cpm/test_data/test_one_critical_path.txt")

# def test_exercise_2():
#     runner("cpm/test_data/exercise_2_test.txt")

# def test_two_critical_paths_that_ends_with_orphans():
#     runner("cpm/test_data/test_two_critical_paths_that_ends_with_orphans.txt")

