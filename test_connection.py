import os.path

import pytest

from graph import Graph


@pytest.fixture()
def graph_1():
    g = Graph("test")
    yield g

    del g
    os.remove("test_nodes.json")
    os.remove("test_connections.json")


def test_create_read_connection(graph_1):
    conn_id = graph_1.add_connection("Andrew", "has title", "Chief Engineer")

    assert graph_1.has_node("Andrew")
    assert graph_1.has_node("Chief Engineer")
    assert graph_1.has_connection("has title")

    got_conn_ids = graph_1.get_connection_ids("has title")
    assert conn_id in got_conn_ids
