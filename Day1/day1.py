import re
from collections.abc import Callable
from typing import Final

PATH_TO_FILE: Final[str] = "./Day1/input_file.txt"

NUMBER_MAPPING: Final[dict[str, str]] = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}


def import_data(path_to_file: str) -> list[str]:
    return [line.rstrip("\n") for line in open(path_to_file, "r+")]


def extract_numerals(string: str, regex_str: str) -> list[str]:
    return re.findall(regex_str, string)


def extract_number(
    string: str, regeg_str, to_numeral: Callable[[str], int] = lambda x: int(x)
) -> int:
    numerals: list[str] = extract_numerals(string, regeg_str)
    return to_numeral(numerals[0]) * 10 + to_numeral(numerals[-1])


def get_sum_of_numerals(
    path_to_file: str,
    regex_str: str,
    to_numeral: Callable[[str], int] = lambda x: int(x),
) -> int:
    data = import_data(path_to_file)
    total_sum: int = 0
    for row in data:
        total_sum += extract_number(row, regex_str, to_numeral)
    return total_sum


def to_numeral(string: str) -> int:
    if string.isdigit():
        return int(string)
    if string not in NUMBER_MAPPING:
        raise ValueError("SNAFU")
    return NUMBER_MAPPING[string]


if __name__ == "__main__":
    print("PART1")
    r = r"\d"
    print(get_sum_of_numerals(PATH_TO_FILE, r))

    print("PART2")
    r = r"(?=(one|two|three|four|five|six|seven|eight|nine|\d))"
    print(get_sum_of_numerals(PATH_TO_FILE, r, to_numeral))
