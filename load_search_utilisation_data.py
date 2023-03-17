from graph import Graph


def parse_staff_list_line(line) -> tuple:
    data = line.strip().split(',')
    return tuple(data[:3])


def load_staff_list(a_graph: Graph, filename: str) -> int:
    lines_processed = 0
    with open(filename) as csv_file:
        for _ in range(9):
            line = csv_file.readline()
        while line:
            name, gm, employment_type = parse_staff_list_line(line)
            if name == "" or gm == "" or employment_type == "":
                line = csv_file.readline()
                continue
            a_graph.add_connection(name, "under GM", gm)
            a_graph.add_connection(name, "employed as", employment_type)
            lines_processed += 1
            line = csv_file.readline()
    return lines_processed


if __name__ == "__main__":
    knowledge_graph = Graph("knowledge")
    file_name = "./Utilisation report - 20230227.xlsx - Staff List.csv"
