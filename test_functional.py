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

def set_up_data(graph:Graph):
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
    graph.add_connection("Chris", "has title", "Senior SRE")
    graph.add_connection("Chris", "works on", "GDT")
    graph.add_connection("Chris", "knows", "Java")
    graph.add_connection("Chris", "knows", "Mulesoft")


def test_full_CRUD_use_case(graph):

    set_up_data(graph)

    # check graph size
    assert graph.count_connections() == 16
    assert graph.count_nodes() == 13

