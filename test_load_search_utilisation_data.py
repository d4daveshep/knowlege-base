import os

import pytest

from graph import Graph
from load_search_utilisation_data import load_staff_list


@pytest.fixture
def utilisation_graph():
    g = Graph("utilisation")
    yield g

    del g
    os.remove("utilisation.json")


def test_load_staff_list(utilisation_graph):
    filename = "./Utilisation report - 20230227.xlsx - Staff List.csv"
    lines_processed = load_staff_list(utilisation_graph, filename)
    assert lines_processed == 181

    assert utilisation_graph.count_connections() == 362
    assert utilisation_graph.has_connection("Aaron Ooi", "under GM", "Dan Cornwall")
    assert utilisation_graph.has_connection("Zoe Xu", "under GM", "Malen Hurbuns")


def test_load_time_by_tasks(utilisation_graph):
    assert False  # TODO
