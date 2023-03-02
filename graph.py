from pysondb import PysonDB


class Graph:
    def __init__(self, filename: str):
        self.db = PysonDB(filename)

    def add_node(self, name: str) -> str:
        return self.db.add({"type": "node", "name": name})

    def has_node(self, name:str) -> bool:
        got = self.db.get_by_query(query=lambda x: x["name"] == name)
        return len(got) > 0


def get_by_name(name: str, data: dict) -> bool:
    return data["name"] == name
