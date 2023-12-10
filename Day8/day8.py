import re
from dataclasses import dataclass
from typing import Final

PATH_TO_FILE: Final[str] = "./Day8/input_file.txt"
PATH_TO_TEST_FILE: Final[str] = "./Day8/test_file.txt"


@dataclass
class Node:
    name: str
    left: str
    right: str


def create_node(record: str) -> Node:
    node_info = re.findall(r"[A-Z]+", record)
    return Node(node_info[0], node_info[1], node_info[2])


def load_data(path_to_file: str) -> tuple[str, dict[str, Node]]:
    nodes: dict[str, Node] = {}
    with open(path_to_file, "r") as file:
        command: str = file.readline().rstrip()
        file.readline()
        for node_str in file.readlines():
            node = create_node(node_str)
            nodes[node.name] = node
    return command, nodes


def traverse_to_ZZZ(command: str, nodes: dict[str, Node], start: str) -> int:
    step = 0
    node = nodes[start]
    count = 0
    while node.name != "ZZZ":
        if step == len(command):
            step = 0

        if command[step] == "R":
            node = nodes[node.right]
        else:
            node = nodes[node.left]

        step += 1
        count += 1
    return count


if __name__ == "__main__":
    print("PART 1")
    command, nodes = load_data(PATH_TO_FILE)
    print(traverse_to_ZZZ(command, nodes, "AAA"))
