from pysondb import PysonDB


class Graph:
    def __init__(self, filename: str):
        self.db = PysonDB(filename)
        self.db.add_new_key(key="type",default="str")
        self.db.add_new_key(key="name",default="str")
        self.db.add_new_key(key="subject_id",default="str")
        self.db.add_new_key(key="target_id",default="str")



    def add_node(self, name: str) -> str:
        node_id = self.get_node_id(name)
        if not node_id:
            return self.db.add(
                {
                    "type": "node",
                    "name": name
                })
        else:
            return node_id

    def has_node(self, name: str) -> bool:
        node_id = self.get_node_id(name)
        return len(node_id) > 0

    def get_node_id(self, name: str) -> str:
        got = self.db.get_by_query(query=lambda n: n["name"] == name)
        if len(got):
            return list(got.keys())[0]
        else:
            return ""

    def add_connection(self, subject: str, connection_name: str, target: str) -> str:
        subject_id = self.add_node(subject)
        target_id = self.add_node(target)

        conn_id = self.db.add(
            {
                "type": "connection",
                "name": connection_name,
                "subject_id": subject_id,
                "target_id": target_id
            })
        return conn_id
