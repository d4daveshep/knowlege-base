import os.path

import pytest
from pysondb import PysonDB


@pytest.fixture
def db_test():
    db = PysonDB("test.json")
    yield db
    del db
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


class Graph:
    def __init__(self, filename:str):
        self.db = PysonDB(filename)



def test_create_graph():
    g = Graph("test.json")
    os.path.isfile("test.json")
    os.remove("test.json")