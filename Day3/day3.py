from __future__ import annotations

import math
import re
from dataclasses import dataclass
from typing import Final

PATH_TO_FILE: Final[str] = "./Day3/input_file.txt"
TEST_FILE: Final[str] = "./Day3/test_input.txt"

SQRT_2: Final[float] = math.sqrt(2)

@dataclass
class Location:
    x: int
    y: int

    def eucledian_distance_to(self, other: Location) -> int:
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)


def import_data(path_to_file: str) -> list[str]:
    return [line.rstrip("\n") for line in open(path_to_file, "r+")]


def is_symbol(char: str) -> bool:
    return not (char.isdigit() or char == ".")


def get_symbol_indices(record: str) -> list[int]:
    return [index for index, char in enumerate(record) if is_symbol(char)]


def extract_symbol_locations(data: list[str]) -> list[Location]:
    indices: list[int] = []
    for index, row in enumerate(data):
        x_values = get_symbol_indices(row)
        indices += [Location(x, index) for x in x_values]
    return indices

def extract_numbers(record: str, row_number: int, symbols: list[Location]) -> list[int]:
    numbers: list[str] = re.findall(r"\d+", record)
    return [
        int(number)
        for number in numbers
        if is_adjecent_to_symbol(number, record, row_number, symbols)
    ]

def is_adjecent_to_symbol(
    number: str, record: str, row_number: int, symbols: list[Location]
):
    index = record.find(number)
    number_length = len(number)
    return any(
        symbol.eucledian_distance_to(Location(index + offset, row_number)) <= SQRT_2
        for symbol in symbols
        for offset in range(number_length)
        if row_number - 1
        <= symbol.y
        <= row_number + 1
    )

def sum_numbers_next_to_symbols(path_to_file: str) -> int:
    data = import_data(path_to_file)
    symbol_locations = extract_symbol_locations(data)
    total = 0
    for row_index, record in enumerate(data):
        total += sum(n for n in extract_numbers(record, row_index, symbol_locations))
    return total

if __name__ == "__main__":
    print("PART 1")
    print(sum_numbers_next_to_symbols(TEST_FILE))


