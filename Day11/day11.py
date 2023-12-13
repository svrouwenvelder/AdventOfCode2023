from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Final

PATH_TO_FILE: Final[str] = "./Day11/input_file.txt"

Map = list[list[str]]


@dataclass
class Location:
    row: int
    column: int

    def manhattan_distance_to(self, other: Location):
        return abs(other.row - self.row) + abs(other.column - self.column)


def read_star_map(path_to_file: str) -> Map:
    return open(path_to_file, "r").read().rstrip().splitlines()


def extract_galaxies(map: Map) -> list[Location]:
    locations: list[Location] = []
    for row_number, row in enumerate(map):
        locations += [
            Location(row=row_number, column=m.start()) for m in re.finditer("#", row)
        ]
    return locations


def correct_galaxy_for_expansion(
    map: Map, galaxies: list[Location], factor: int = 1
) -> Map:
    rows_with_galaxies: set[int] = set()
    columns_with_galaxies: set[int] = set()
    galaxy: Location
    for galaxy in galaxies:
        rows_with_galaxies.add(galaxy.row)
        columns_with_galaxies.add(galaxy.column)

    rows_without_galaxies: list[int] = [
        i for i in range(0, len(map)) if i not in rows_with_galaxies
    ]
    columns_without_galaxies: list[int] = [
        i for i in range(0, len(map[0])) if i not in columns_with_galaxies
    ]

    return [
        _correct_galaxy(galaxy, rows_without_galaxies, columns_without_galaxies, factor)
        for galaxy in galaxies
    ]


def _correct_galaxy(
    galaxy_location: Location,
    rows_without_galaxies: list[int],
    columns_without_galaxies: list[int],
    factor: int,
) -> Location:
    empty_rows_before = len(
        [i for i in rows_without_galaxies if i < galaxy_location.row]
    )
    empty_columns_before = len(
        [i for i in columns_without_galaxies if i < galaxy_location.column]
    )
    return Location(
        row=galaxy_location.row + empty_rows_before * factor,
        column=galaxy_location.column + empty_columns_before * factor,
    )


def get_summed_manhattan_distance(galaxies: list[Location]) -> int:
    total: int = 0
    for galaxy_number, galaxy in enumerate(galaxies):
        for other_galaxy in galaxies[galaxy_number + 1 :]:
            total += galaxy.manhattan_distance_to(other_galaxy)
    return total


if __name__ == "__main__":
    print("PART 1")
    map = read_star_map(PATH_TO_FILE)
    original_galaxies = extract_galaxies(map)
    galaxies = correct_galaxy_for_expansion(map, original_galaxies, factor=1)
    print(get_summed_manhattan_distance(galaxies))

    print(" ")
    print("PART 2")
    galaxies = correct_galaxy_for_expansion(map, original_galaxies, factor=1000000 - 1)
    print(get_summed_manhattan_distance(galaxies))
