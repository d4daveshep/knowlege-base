import os

import pytest

from graph import Graph


@pytest.fixture
def utilisation_graph():
    g = Graph("utilisation")
    yield g

    # del g
    # os.remove("utilisation_connections.json")

def parse_staff_list_line(line) -> tuple:
    data = line.strip().split(',')
    return tuple(data[:3])


def test_load_staff_list(utilisation_graph):
    with open("./Utilisation report - 20230227.xlsx - Staff List.csv") as csv_file:
        for _ in range(9):
            line = csv_file.readline()
        while line:
            name, gm, employment_type = parse_staff_list_line(line)
            if (name == "" or gm=="" or employment_type==""):
                line = csv_file.readline()
                continue
            utilisation_graph.add_connection(name, "under GM", gm)
            utilisation_graph.add_connection(name, "employed as", employment_type)
            line = csv_file.readline()

    assert utilisation_graph.count_connections() == 362
    assert utilisation_graph.has_connection("Aaron Ooi", "under GM", "Dan Cornwall")
    assert utilisation_graph.has_connection("Zoe Xu", "under GM", "Malen Hurbuns")


