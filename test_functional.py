import os

import pytest

from graph import Graph


@pytest.fixture()
def graph():
    g = Graph("test")

    # counts should be: 16 connections, 13 nodes

    yield g

    del g
    # os.remove("test_nodes.json")
    os.remove("test_connections.json")


def set_up_data(graph: Graph):
    graph.add_connection("Andrew", "is a", "Permanent Employee")
    graph.add_connection("Andrew", "has title", "Chief Engineer")
    graph.add_connection("Andrew", "worked on", "TWG")
    graph.add_connection("Andrew", "worked on", "GDT")
    graph.add_connection("Andrew", "knows", "Java")
    graph.add_connection("Andrew", "knows", "Spring Boot")

    graph.add_connection("Chris", "is a", "Contractor")
    graph.add_connection("Chris", "has title", "Senior Software Engineer")
    graph.add_connection("Chris", "works on", "GDT")
    graph.add_connection("Chris", "knows", "Java")
    graph.add_connection("Chris", "knows", "Mulesoft")

    graph.add_connection("Paul", "is a", "Permanent Employee")
    graph.add_connection("Paul", "has title", "Senior SRE")
    graph.add_connection("Paul", "works on", "GDT")
    graph.add_connection("Paul", "knows", "Java")
    graph.add_connection("Paul", "knows", "Mulesoft")


def test_full_CRUD_use_case(graph):
    set_up_data(graph)

    # check graph size
    assert graph.count_connections() == 16
    assert graph.count_nodes() == 13

    # search for connections to Andrew
    conns = graph.get_connection_data_to_node("Andrew")
    assert len(conns) == 6

    # check targets
    targets = {conn["target"] for conn in conns}
    assert len(targets) == 6
    assert "Permanent Employee" in targets
    assert "Chief Engineer" in targets
    assert "TWG" in targets
    assert "GDT" in targets
    assert "Java" in targets
    assert "Spring Boot" in targets
    assert not "Mulesoft" in targets
    assert not "Senior SRE" in targets

    # check connection names
    names = {conn["name"] for conn in conns}
    assert len(names) == 4
    assert "is a" in names
    assert "has title" in names
    assert "worked on" in names
    assert "knows" in names

    # find connections to Java
    conns = graph.get_connection_data_to_node("java")  # lower case should work
    assert len(conns) == 3

    # check subjects
    targets = {conn["subject"] for conn in conns}
    assert "Andrew" in targets
    assert "Chris" in targets
    assert "Paul" in targets

    # check connection names
    names = {conn["name"] for conn in conns}
    assert len(names) == 1
    assert "knows" in names

    # find who knows what
    conns = graph.get_connections_named("knows")
    assert len(conns) == 6

    # check pairs
    pairs = {(conn["subject"], conn["target"]) for conn in conns}
    assert len(pairs) == 6
    assert ("Andrew", "Java") in pairs
    assert ("Chris", "Java") in pairs
    assert ("Paul", "Java") in pairs
    assert ("Andrew", "Spring Boot") in pairs
    assert ("Chris", "Mulesoft") in pairs
    assert ("Paul", "Mulesoft") in pairs
