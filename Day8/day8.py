import math
import re
from collections.abc import Callable
from dataclasses import dataclass
from typing import Final

PATH_TO_FILE: Final[str] = "./Day8/input_file.txt"


@dataclass
class Node:
    name: str
    left: str
    right: str


def create_node(record: str) -> Node:
    node_info = re.findall(r"[\w\d]+", record)
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


def traverse(
    command: str,
    nodes: dict[str, Node],
    start: str,
    terminal_condition: Callable[[str], bool],
) -> int:
    step = 0
    node = nodes[start]
    count = 0
    while not terminal_condition(node.name):
        if step == len(command):
            step = 0

        if command[step] == "R":
            node = nodes[node.right]
        else:
            node = nodes[node.left]

        step += 1
        count += 1
    return count


def get_starting_nodes(nodes: list[str]) -> list[str]:
    return [node for node in nodes if node[-1] == "A"]


if __name__ == "__main__":
    print("PART 1")
    terminal_condition = lambda x: x == "ZZZ"
    command, nodes = load_data(PATH_TO_FILE)
    print(traverse(command, nodes, "AAA", terminal_condition))

    print("PART 2")
    # there is a noticable sequence in the path of each starting point. 
    terminal_condition = lambda x: x[-1] == "Z"
    loops = [
        traverse(command, nodes, start, terminal_condition)
        for start in get_starting_nodes(list(nodes.keys()))
    ]
    print(math.lcm(*loops))
