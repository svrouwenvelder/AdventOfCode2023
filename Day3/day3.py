from __future__ import annotations

import math
import re
from collections.abc import Callable
from dataclasses import dataclass
from typing import Final

PATH_TO_FILE: Final[str] = "./Day3/input_file.txt"


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


def is_star(char: str) -> bool:
    return char == "*"


def get_symbol_indices(
    record: str, is_symbol_of_interest: Callable[[str], bool]
) -> list[int]:
    return [index for index, char in enumerate(record) if is_symbol_of_interest(char)]


def extract_symbol_locations(
    data: list[str], is_symbol_of_interest: Callable[[str], bool] = is_symbol
) -> list[Location]:
    indices: list[int] = []
    for index, row in enumerate(data):
        x_values = get_symbol_indices(row, is_symbol_of_interest)
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


def sum_numbers_next_to_starts(path_to_file: str) -> int:
    data = import_data(path_to_file)
    star_locations = extract_symbol_locations(data, is_star)
    total = 0
    for location in star_locations:
        numbers = get_adjecent_numbers(location, data)
        if len(numbers) == 2:
            total += numbers[0] * numbers[1]
    return total


def get_adjecent_numbers(location: Location, data):
    numbers = []
    for row_nr in range(location.y - 1, location.y + 2):
        numbers += extract_numbers(data[row_nr], row_nr, [location])
    return numbers


if __name__ == "__main__":
    print("PART 1")
    print(sum_numbers_next_to_symbols(PATH_TO_FILE))

    print("PART 2")
    print(sum_numbers_next_to_starts(PATH_TO_FILE))
