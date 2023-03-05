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


def test_create_read_new_node(graph_1):
    graph_1.add_node("Andrew")
    assert graph_1.has_node("Andrew")


def test_cant_read_non_existent_node(graph_1):
    graph_1.add_node("Chris")
    assert not graph_1.has_node("Andrew")


def test_dont_create_duplicate_node(graph_1):
    andrew_id_1 = graph_1.add_node("Andrew")
    andrew_id_2 = graph_1.add_node("Andrew")
    assert andrew_id_1 == andrew_id_2


def test_get_node(graph_1):
    andrew_id = graph_1.add_node("Andrew")
    chris_id = graph_1.add_node("Chris")
    paul_id = graph_1.add_node("Paul")

    assert andrew_id == graph_1.get_node_id("Andrew")
    assert chris_id == graph_1.get_node_id("Chris")
    assert paul_id == graph_1.get_node_id("Paul")


def test_update_node(graph_1):
    andrew_id = graph_1.add_node("Andrew")
    graph_1.update_node("Andrew", "Paul")
    paul_id = graph_1.get_node_id("Paul")
    assert paul_id == andrew_id


def test_delete_node(graph_1):
    andrew_id = graph_1.add_node("Andrew")
    assert len(andrew_id)

    graph_1.delete_node("Andrew")
    andrew_id = graph_1.get_node_id("Andrew")
    assert not andrew_id


def test_delete_node_deletes_connections():
    # TODO
    assert False
