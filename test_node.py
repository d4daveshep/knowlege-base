import os.path

import pytest

from graph import Graph


@pytest.fixture()
def graph_1():
    g = Graph("test")
    yield g

    del g
    os.remove("test_connections.json")


def test_has_node(graph_1):
    conn_id = graph_1.add_connection("Andrew", "has title", "Chief Engineer")
    assert graph_1.has_node("Andrew")
    assert graph_1.has_node("andrew")


def test_cant_read_non_existent_node(graph_1):
    conn_id = graph_1.add_connection("Andrew", "has title", "Chief Engineer")
    assert not graph_1.has_node("Paul")


def test_update_node(graph_1):
    conn_id = graph_1.add_connection("Andrew", "has title", "Chief Engineer")
    graph_1.update_node("Andrew", "Paul")
    assert graph_1.has_node("Paul")
    assert not graph_1.has_node("Andrew")

    graph_1.update_node("paul", "David")  # test case-insensitive
    assert graph_1.has_node("david")
    assert not graph_1.has_node("Paul")

    assert graph_1.count_connections() == 1


def test_delete_node_deletes_connections(graph_1):
    conn_id_1 = graph_1.add_connection("Andrew", "has title", "Chief Engineer")
    conn_id_2 = graph_1.add_connection("Andrew", "worked on", "TWG")
    conn_id_3 = graph_1.add_connection("Andrew", "knows", "Java")
    conn_id_4 = graph_1.add_connection("Andrew", "knows", "Spring Boot")

    graph_1.delete_node("Java")
    assert not graph_1.has_node("Java")
    assert len(graph_1.get_connection_ids_named("knows")) == 1
    assert not graph_1.has_connection("Andrew", "knows", "Java")

    graph_1.delete_node("twg")
    assert not graph_1.has_node("TWG")
