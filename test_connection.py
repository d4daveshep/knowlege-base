import os.path

import pytest
from pysondb.errors import IdDoesNotExistError

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
    assert graph_1.has_connection_named("has title")
    assert graph_1.has_connection("Andrew", "has title", "Chief Engineer")

    got_conn_ids = graph_1.get_connection_ids_named("has title")
    assert conn_id in got_conn_ids


def test_create_read_multiple_connections(graph_1):
    conn_id_1 = graph_1.add_connection("Andrew", "has title", "Chief Engineer")
    conn_id_2 = graph_1.add_connection("Andrew", "worked on", "TWG")
    conn_id_3 = graph_1.add_connection("Andrew", "knows", "Java")
    conn_id_4 = graph_1.add_connection("Andrew", "knows", "Spring Boot")

    assert graph_1.has_connection_named("has title")
    assert graph_1.has_connection_named("worked on")
    assert graph_1.has_connection_named("knows")

    got_conn_ids = graph_1.get_connection_ids_named("knows")
    assert len(got_conn_ids) == 2
    assert conn_id_3 in got_conn_ids
    assert conn_id_4 in got_conn_ids


def test_delete_connection_by_id(graph_1):
    conn_id_1 = graph_1.add_connection("Andrew", "has title", "Chief Engineer")
    conn_id_2 = graph_1.add_connection("Andrew", "worked on", "TWG")
    conn_id_3 = graph_1.add_connection("Andrew", "knows", "Java")
    conn_id_4 = graph_1.add_connection("Andrew", "knows", "Spring Boot")

    graph_1.delete_connection_by_id(conn_id_3)
    got_conn_ids = graph_1.get_connection_ids_named("knows")
    assert len(got_conn_ids) == 1
    assert conn_id_3 not in got_conn_ids
    assert conn_id_4 in got_conn_ids


def test_cant_delete_nonexistent_connection(graph_1):
    conn_id_1 = graph_1.add_connection("Andrew", "has title", "Chief Engineer")

    with pytest.raises(IdDoesNotExistError):
        graph_1.delete_connection_by_id("fake_id")

    with pytest.raises(IdDoesNotExistError):
        graph_1.delete_connection("Paul", "has title", "Chief Engineer")
    with pytest.raises(IdDoesNotExistError):
        graph_1.delete_connection("Andrew", "has title", "Senior Engineer")
    with pytest.raises(IdDoesNotExistError):
        graph_1.delete_connection("Andrew", "is a", "Chief Engineer")

    assert True


def test_delete_connection(graph_1):
    conn_id_1 = graph_1.add_connection("Andrew", "has title", "Chief Engineer")
    conn_id_2 = graph_1.add_connection("Andrew", "worked on", "TWG")
    conn_id_3 = graph_1.add_connection("Andrew", "knows", "Java")
    conn_id_4 = graph_1.add_connection("Andrew", "knows", "Spring Boot")

    graph_1.delete_connection("Andrew", "has title", "Chief Engineer")
    assert not graph_1.has_connection_named("has title")

    graph_1.delete_connection("Andrew", "knows", "Java")
    assert graph_1.has_connection_named("knows")

    assert not graph_1.has_connection("Andrew", "knows", "Java")
    assert graph_1.has_connection("Andrew", "knows", "Spring Boot")

def test_get_connections_to_node(graph_1):
    conn_id_1 = graph_1.add_connection("Andrew", "has title", "Chief Engineer")
    conn_id_2 = graph_1.add_connection("Andrew", "worked on", "TWG")
    conn_id_3 = graph_1.add_connection("Andrew", "knows", "Java")
    conn_id_4 = graph_1.add_connection("Andrew", "knows", "Spring Boot")

    andrew_connections = graph_1.get_connections_to_node("Andrew")
    assert len(andrew_connections) == 4
    assert conn_id_1 in andrew_connections
    assert conn_id_2 in andrew_connections
    assert conn_id_3 in andrew_connections
    assert conn_id_4 in andrew_connections

    java_connections = graph_1.get_connections_to_node("Java")
    assert len(java_connections) == 1
    assert conn_id_3 in java_connections


