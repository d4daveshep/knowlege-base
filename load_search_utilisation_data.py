from graph import Graph


def parse_staff_list_line(line) -> tuple:
    data = line.strip().split(',')
    return tuple(data[:3])


if __name__ == "__main__":
    knowledge_graph = Graph("knowledge")

    with open("./Utilisation report - 20230227.xlsx - Staff List.csv") as csv_file:
        for _ in range(9):
            line = csv_file.readline()
        while line:
            name, gm, employment_type = parse_staff_list_line(line)
            if name == "" or gm == "" or employment_type == "":
                line = csv_file.readline()
                continue
            knowledge_graph.add_connection(name, "under GM", gm)
            knowledge_graph.add_connection(name, "employed as", employment_type)
            line = csv_file.readline()
