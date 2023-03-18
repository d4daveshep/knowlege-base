from graph import Graph


def parse_staff_list_line(line) -> tuple:
    data = line.strip().split(',')
    return tuple(
        data[:3]  # person name, GM, employment type
    )


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


def parse_time_by_task_line(line) -> tuple:
    data = line.strip().split(',')
    return tuple([
        data[0],  # client name
        data[2],  # job name (incl code)
        data[5],  # person name
        data[7],  # date
        data[9],  # hours
    ])


def load_time_by_task(a_graph: Graph, filename: str) -> int:
    lines_processed = 0
    with open(filename) as csv_file:
        for _ in range(2):
            line = csv_file.readline()
        while line:
            client, job, name, date, hours = parse_time_by_task_line(line)

            a_graph.add_connection(name, "worked on", client)
            a_graph.add_connection(name, "billed time to", job)
            a_graph.add_connection(client, "has job", job)
            lines_processed += 1
            line = csv_file.readline()

    return lines_processed


if __name__ == "__main__":
    knowledge_graph = Graph("knowledge")
    staff_list_file = "./Utilisation report - 20230227.xlsx - Staff List.csv"
    load_staff_list(knowledge_graph, staff_list_file)

    time_by_task_file = "./Utilisation report - 20230227.xlsx - TimeByTask.csv"
    load_time_by_task(knowledge_graph, time_by_task_file)
