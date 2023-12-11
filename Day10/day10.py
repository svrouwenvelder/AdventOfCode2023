from __future__ import annotations

from dataclasses import dataclass
from typing import Final

PATH_TO_FILE: Final[str] = "./Day10/input_file.txt"
PATH_TO_TEST_FILE: Final[str] = "./Day10/test_file.txt"


@dataclass
class Vector2D:
    x: int
    y: int


@dataclass
class Position:
    row: int
    column: int

    def move(self, direction: Vector2D) -> Position:
        return Position(row=self.row + direction.y, column=self.column + direction.x)


@dataclass
class Maze:
    field: list[list[str]]

    def get_element(self, position: Position) -> str:
        return self.field[position.row][position.column]

    @property
    def start_position(self) -> Position:
        for row_number, row in enumerate(self.field):
            for collumn_number, element in enumerate(row):
                if element == "S":
                    return Position(row_number, collumn_number)


NORTH: Final[Vector2D] = Vector2D(0, -1)
SOUTH: Final[Vector2D] = Vector2D(0, 1)
EAST: Final[Vector2D] = Vector2D(1, 0)
WEST: Final[Vector2D] = Vector2D(-1, 0)


def get_next_vector(current_vector: Vector2D, element: str) -> Vector2D:
    if element == "-" or element == "|":
        return current_vector
    if element == "7":
        return SOUTH if current_vector == EAST else WEST
    if element == "F":
        return SOUTH if current_vector == WEST else EAST
    if element == "L":
        return EAST if current_vector == SOUTH else NORTH
    if element == "J":
        return WEST if current_vector == SOUTH else NORTH


def import_maze(path_to_file: str) -> Maze:
    return Maze(open(path_to_file, "r").read().rstrip().splitlines())


def get_next_option(maze: Maze, start_position: Position, direction: Vector2D) -> str:
    return maze.get_element(start_position.move(direction))


def initial_direction(
    maze: Maze, start_position: Position
) -> tuple[Vector2D, Position, str]:
    if (element := get_next_option(maze, start_position, NORTH)) in ["|", "7", "F"]:
        return (NORTH, start_position.move(NORTH), element)
    if (element := get_next_option(maze, start_position, EAST)) in ["-", "7"]:
        return (EAST, start_position.move(EAST), element)
    if (element := get_next_option(maze, start_position, SOUTH)) in ["|", "L"]:
        return (SOUTH, start_position.move(SOUTH), element)
    if (element := get_next_option(maze, start_position, WEST)) in ["-", "F"]:
        return (WEST, start_position.move(WEST), element)
    raise ValueError("SNAFU")


def get_length(maze: Maze) -> int:
    current_direction, current_position, element = initial_direction(
        maze, maze.start_position
    )
    count: int = 0
    while element != "S":
        current_direction = get_next_vector(current_direction, element)
        current_position = current_position.move(current_direction)
        element = maze.get_element(current_position)
        count += 1
    return count + 1


if __name__ == "__main__":
    print("PART 1")
    print(get_length(import_maze(PATH_TO_FILE)) / 2)
