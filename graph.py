from collections import Counter

from pysondb import PysonDB


class Graph:
    def __init__(self, filename: str):
        self.connections_db = PysonDB(f"{filename}_connections.json")

        # # define schemas
        # self.connections_db.add_new_key(key="name", default="str")
        # self.connections_db.add_new_key(key="subject", default="str")
        # self.connections_db.add_new_key(key="target", default="str")


    def has_node(self, name: str) -> bool:
        got = self.connections_db.get_by_query(
            query=lambda c: c["subject"] == name or
                            c["target"] == name
        )
        return len(got) > 0

    def update_node(self, from_name: str, to_name: str) -> None:
        conn_ids = self.get_connections_to_node(from_name)
        for conn_id in conn_ids:
            conn = self.connections_db.get_by_id(conn_id)
            if conn["subject"] == from_name:
                conn["subject"] = to_name
            if conn["target"] == from_name:
                conn["target"] = to_name
            self.connections_db.update_by_id(conn_id,conn)

    def delete_node(self, name: str) -> None:
        # delete the connections first
        conn_ids = self.get_connections_to_node(name)
        for conn_id in conn_ids:
            self.connections_db.delete_by_id(conn_id)

    def add_connection(self, subject: str, connection_name: str, target: str) -> str:
        conn_id = self.connections_db.add(
            {
                "name": connection_name,
                "subject": subject,
                "target": target
            })
        return conn_id

    def has_connection_named(self, name: str) -> bool:
        conn_id = self.get_connection_ids_named(name)
        return len(conn_id) > 0

    def has_connection(self, subject: str, connection_name: str, target: str) -> bool:
        got = self.connections_db.get_by_query(
            query=lambda c: c["subject"] == subject and
                            c["name"] == connection_name and
                            c["target"] == target
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
        got = self.connections_db.get_by_query(
            query=lambda c: c["subject"] == subject and
                            c["name"] == connection_name and
                            c["target"] == target
        )
        if len(got):
            return list(got.keys())[0]
        else:
            return ""

    def get_connections_to_node(self, node_name: str) -> list:
        got = self.connections_db.get_by_query(
            query=lambda c: c["subject"] == node_name or
                            c["target"] == node_name
        )
        if len(got) > 0:
            return list(got.keys())
        else:
            return []

    def count_connections(self) -> int:
        return len(self.connections_db.get_all())

    def count_nodes(self) -> int:
        all = self.connections_db.get_all()
        nodes = set()
        for conn in all.values():
            nodes.add(conn["subject"])
            nodes.add(conn["target"])
        return len(nodes)
