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


def test_create_read_one_connection(graph_1):
    conn_id = graph_1.add_connection("Andrew", "has title", "Chief Engineer")

    assert graph_1.has_node("Andrew")
    assert graph_1.has_node("Chief Engineer")
    assert graph_1.has_connection("has title")

    got_conn_ids = graph_1.get_connection_ids("has title")
    assert conn_id in got_conn_ids

def test_create_read_multiple_connections(graph_1):
    conn_id_1 = graph_1.add_connection("Andrew", "has title", "Chief Engineer")
    conn_id_2 = graph_1.add_connection("Andrew", "worked on", "TWG")
    conn_id_3 = graph_1.add_connection("Andrew", "knows", "Java")
    conn_id_4 = graph_1.add_connection("Andrew", "knows", "Spring Boot")

    assert graph_1.has_connection("has title")
    assert graph_1.has_connection("worked on")
    assert graph_1.has_connection("knows")

    got_conn_ids = graph_1.get_connection_ids("knows")
    assert len(got_conn_ids) == 2
    assert conn_id_3 in got_conn_ids
    assert conn_id_4 in got_conn_ids

