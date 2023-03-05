from pysondb import PysonDB


class Graph:
    def __init__(self, filename: str):
        self.nodes_db = PysonDB(f"{filename}_nodes.json")
        self.connections_db = PysonDB(f"{filename}_connections.json")

        # define schemas
        self.nodes_db.add_new_key(key="name", default="str")
        self.connections_db.add_new_key(key="name", default="str")
        self.connections_db.add_new_key(key="subject_id", default="str")
        self.connections_db.add_new_key(key="target_id", default="str")

    def add_node(self, name: str) -> str:
        node_id = self.get_node_id(name)
        if not node_id:
            return self.nodes_db.add({"name": name})
        else:
            return node_id

    def has_node(self, name: str) -> bool:
        node_id = self.get_node_id(name)
        return len(node_id) > 0

    def get_node_id(self, name: str) -> str:
        got = self.nodes_db.get_by_query(query=lambda n: n["name"] == name)
        if len(got):
            return list(got.keys())[0]
        else:
            return ""

    def update_node(self, from_name: str, to_name: str) -> None:
        node_id = self.get_node_id(from_name)
        self.nodes_db.update_by_id(node_id, {"name": to_name})

    def delete_node(self, name: str) -> None:
        node_id = self.get_node_id(name)
        self.nodes_db.delete_by_id(node_id)

    def add_connection(self, subject: str, connection_name: str, target: str) -> str:
        subject_id = self.add_node(subject)
        target_id = self.add_node(target)

        conn_id = self.connections_db.add(
            {
                "name": connection_name,
                "subject_id": subject_id,
                "target_id": target_id
            })
        return conn_id

    def has_connection(self, name: str) -> bool:
        conn_id = self.get_connection_ids(name)
        return len(conn_id) > 0

    def get_connection_ids(self, name: str) -> str:
        got = self.connections_db.get_by_query(query=lambda n: n["name"] == name)
        if len(got):
            return list(got.keys())[0]
        else:
            return ""
