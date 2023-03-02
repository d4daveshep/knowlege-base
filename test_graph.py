import os.path

import pytest
from pysondb import PysonDB

from graph import Graph


@pytest.fixture
def db_test():
    db = PysonDB("test.json")
    yield db
    del db
    os.remove("test.json")


@pytest.fixture()
def graph_1():
    g = Graph("test.json")
    yield g

    del g
    os.remove("test.json")


def test_create_db(db_test):
    assert os.path.isfile("test.json")


def test_add_node_to_db(db_test):
    node = {"type": "node", "name": "Andrew"}
    node_id = db_test.add(node)
    assert db_test.get_by_id(node_id) == node


def test_get_node_by_name(db_test):
    node = {"type": "node", "name": "Andrew"}
    db_test.add(node)

    got = db_test.get_by_query(query=lambda x: x["name"] == "Andrew")
    assert len(got) == 1
    values = list(got.values())
    assert list(got.values())[0]["name"] == "Andrew"

    pass


def test_create_graph():
    g = Graph("test.json")
    os.path.isfile("test.json")
    os.remove("test.json")


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
