from __future__ import annotations

import math
import re
from dataclasses import dataclass
from typing import Final

PATH_TO_FILE: Final[str] = "./Day3/input_file.txt"
TEST_FILE: Final[str] = "./Day3/test_input.txt"


@dataclass
class Location:
    x: int
    y: int

    def eucledian_distance_to(self, other: Location) -> int:
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    def is_adjecent(self, other: Location) -> bool:
        return self.eucledian_distance_to(other) < 2


def import_data(path_to_file: str) -> list[str]:
    return [line.rstrip("\n") for line in open(path_to_file, "r+")]


def is_symbol(char: str) -> bool:
    return not char.isdigit() and char != "."


def get_symbol_indices(record: str) -> list[int]:
    return [index for index, char in enumerate(record) if is_symbol(char)]


def extract_symbol_locations(data: list[str]) -> list[Location]:
    indices: list[int] = []
    for index, row in enumerate(data):
        x_values = get_symbol_indices(row)
        indices += [Location(x, index) for x in x_values]
    return indices


def extract_numbers(record: str, row_number: int, symbols: list[Location]) -> list[int]:
    matches = re.finditer(r"\d+", record)
    return [
        int(match.group())
        for match in matches
        if is_adjecent_to_symbol(match.span(), row_number, symbols)
    ]


def is_adjecent_to_symbol(
    span: tuple[int, int], row_number: int, symbols: list[Location]
):
    return any(
        symbol.is_adjecent(Location(x, row_number))
        for symbol in symbols
        for x in range(span[0], span[1])
        if row_number - 1 <= symbol.y <= row_number + 1
    )


def sum_numbers_next_to_symbols(path_to_file: str) -> int:
    data = import_data(path_to_file)
    symbol_locations = extract_symbol_locations(data)
    total = 0
    for row_index, record in enumerate(data):
        total += sum(extract_numbers(record, row_index, symbol_locations))
    return total


if __name__ == "__main__":
    print("PART 1")
    print(sum_numbers_next_to_symbols(PATH_TO_FILE))
