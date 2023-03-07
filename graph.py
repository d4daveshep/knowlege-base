from collections import Counter

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
        # delete the connections first
        conn_ids = self.get_connections_to_node(name)
        for conn_id in conn_ids:
            self.connections_db.delete_by_id(conn_id)
        # now delete the node
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

    def has_connection_named(self, name: str) -> bool:
        conn_id = self.get_connection_ids_named(name)
        return len(conn_id) > 0

    def has_connection(self, subject: str, connection_name: str, target: str) -> bool:
        subject_id = self.get_node_id(subject)
        target_id = self.get_node_id(target)
        if subject_id == "" or target_id == "":
            return False

        got = self.connections_db.get_by_query(
            query=lambda c: c["subject_id"] == subject_id and
                            c["name"] == connection_name and
                            c["target_id"] == target_id
        )
        return len(got) > 0

    def get_connection_ids_named(self, name: str) -> list:
        got = self.connections_db.get_by_query(query=lambda n: n["name"] == name)
        if len(got):
            return list(got.keys())
        else:
            return []

    def delete_connection_by_id(self, conn_id: str) -> None:
        self.connections_db.delete_by_id(conn_id)

    def delete_connection(self, subject: str, connection_name: str, target: str) -> None:
        conn_id = self.get_connection_id(subject, connection_name, target)
        self.connections_db.delete_by_id(conn_id)

    def get_connection_id(self, subject: str, connection_name: str, target: str) -> str:
        subject_id = self.get_node_id(subject)
        target_id = self.get_node_id(target)
        if subject_id == "" or target_id == "":
            return ""

        got = self.connections_db.get_by_query(
            query=lambda c: c["subject_id"] == subject_id and
                            c["name"] == connection_name and
                            c["target_id"] == target_id
        )
        if len(got):
            return list(got.keys())[0]
        else:
            return ""

    def get_connections_to_node(self, node_name: str) -> list:
        node_id = self.get_node_id(node_name)
        got = self.connections_db.get_by_query(
            query=lambda c: c["subject_id"] == node_id or
                            c["target_id"] == node_id
        )
        if len(got) > 0:
            return list(got.keys())
        else:
            return []

    def count_connections(self) -> int:
        return len(self.connections_db.get_all())

    def count_nodes(self) -> int:
        all = self.connections_db.get_all()
        for conn in all.values():
            pass
        return 0
