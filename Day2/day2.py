import re
from enum import Enum
from typing import Final

PATH_TO_FILE: Final[str] = "./Day2/input_file.txt"

NUMBER_OF_RED_CUBES: Final[int] = 12
NUMBER_OF_GREEN_CUBES: Final[int] = 13
NUMBER_OF_BLUE_CUBES: Final[int] = 14


class CubeColor(str, Enum):
    BLUE = "blue"
    GREEN = "green"
    RED = "red"


def extract_game_id(record: str) -> int:
    return int(re.findall(r"(?<=Game) (\d+)", record)[0])


def is_below_limit(record: str, color: CubeColor, limit: int) -> bool:
    results = extract_color_realisation(record, color)
    if not results:
        return True
    return all(int(r) <= limit for r in results)


def extract_color_realisation(record: str, color: CubeColor):
    results = re.findall(rf"(\d+) (?={color.value})", record)
    return [int(r) for r in results]


def is_feasible(record: str) -> bool:
    return (
        is_below_limit(record, CubeColor.RED, NUMBER_OF_RED_CUBES)
        and is_below_limit(record, CubeColor.BLUE, NUMBER_OF_BLUE_CUBES)
        and is_below_limit(record, CubeColor.GREEN, NUMBER_OF_GREEN_CUBES)
    )


def get_min_required_number_of_cubes(record: str, color: CubeColor) -> int:
    return max(extract_color_realisation(record, color))


def get_cube_power(record: str):
    result = 1
    for color in CubeColor:
        result *= get_min_required_number_of_cubes(record, color)
    return result


def add_feasible_ids(path_to_file: str) -> int:
    with open(path_to_file, "r+") as file:
        return sum(
            [
                extract_game_id(game_record)
                for game_record in file.readlines()
                if is_feasible(game_record)
            ]
        )


def get_summed_cube_power(path_to_file: str) -> int:
    with open(path_to_file, "r+") as file:
        return sum([get_cube_power(game_record) for game_record in file.readlines()])


if __name__ == "__main__":
    print("PART 1")
    print(add_feasible_ids(PATH_TO_FILE))

    print("PART 2")
    print(get_summed_cube_power(PATH_TO_FILE))
