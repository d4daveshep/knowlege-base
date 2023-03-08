import os

import pytest

from graph import Graph


@pytest.fixture()
def graph():
    g = Graph("test")

    g.add_connection("Andrew", "is a", "Permanent Employee")
    g.add_connection("Andrew", "has title", "Chief Engineer")
    g.add_connection("Andrew", "worked on", "TWG")
    g.add_connection("Andrew", "worked on", "GDT")
    g.add_connection("Andrew", "knows", "Java")
    g.add_connection("Andrew", "knows", "Spring Boot")

    g.add_connection("Chris", "is a", "Contractor")
    g.add_connection("Chris", "has title", "Senior Software Engineer")
    g.add_connection("Chris", "works on", "GDT")
    g.add_connection("Chris", "knows", "Java")
    g.add_connection("Chris", "knows", "Mulesoft")

    g.add_connection("Paul", "is a", "Permanent Employee")
    g.add_connection("Chris", "has title", "Senior SRE")
    g.add_connection("Chris", "works on", "GDT")
    g.add_connection("Chris", "knows", "Java")
    g.add_connection("Chris", "knows", "Mulesoft")

    # counts should be: 16 connections, 13 nodes

    yield g

    del g
    # os.remove("test_nodes.json")
    os.remove("test_connections.json")

def test_full_CRUD_use_case(graph):

    # check graph size
    assert graph.count_connections() == 16
    assert graph.count_nodes() == 13

