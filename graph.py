from pysondb import PysonDB


class Graph:
    def __init__(self, filename: str):
        self.db = PysonDB(filename)

    def add_node(self, name: str) -> str:
        node_id = self.get_node_id(name)
        if not node_id:
            return self.db.add({"type": "node", "name": name})
        else:
            return node_id

    def has_node(self, name: str) -> bool:
        node_id = self.get_node_id(name)
        return len(node_id) > 0

    def get_node_id(self, name: str) -> str:
        got = self.db.get_by_query(query=lambda x: x["name"] == name)
        if len(got):
            return list(got.keys())[0]
        else:
            return ""


def get_by_name(name: str, data: dict) -> bool:
    return data["name"] == name
