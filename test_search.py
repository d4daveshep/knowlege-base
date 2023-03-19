import os.path

import pytest

from graph import Graph


def test_search_by_partial_node_name():

    assert os.path.exists("./knowledge.json")

    knowledge_graph = Graph("knowledge")
    assert knowledge_graph.has_node("Andrew Lindesay")
    assert knowledge_graph.has_node("Andrew Campkin")
    assert knowledge_graph.has_node("Andrew Barclay")
    assert knowledge_graph.has_node("Andrew Martin")
    assert knowledge_graph.has_node("Andrew Simpson")
    assert knowledge_graph.has_node("Andrew Wells")

    connections_to_andrew = knowledge_graph.node_search("andrew")


