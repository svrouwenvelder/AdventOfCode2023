import re
from typing import Final

PATH_TO_FILE: Final[str] = "./Day4/input_file.txt"
PATH_TO_TEST_FILE: Final[str] = "./Day4/test_file.txt"


def get_winning_numbers(card_record: str) -> list[int]:
    start = card_record.index(":")
    end = card_record.index("|")
    return _extract_numbers(card_record, start, end)


def get_ticket_numbers(card_record: str) -> list[int]:
    start = card_record.index("|")
    end = len(card_record) - 1
    return _extract_numbers(card_record, start, end)


def _extract_numbers(card_record: str, start: int, end: int) -> list[int]:
    numbers = re.findall(r"\d+", card_record[start:end])
    return [int(n) for n in numbers]


def get_points(number_of_matches: int) -> int:
    if not number_of_matches:
        return 0
    return 2 ** (number_of_matches - 1)


def get_total_points(path_to_file: str) -> int:
    with open(path_to_file, "r+") as file:
        score = 0
        for card in file.readlines():
            score += get_points(
                sum(
                    1
                    for number in get_winning_numbers(card)
                    if number in get_ticket_numbers(card)
                )
            )
    return score


if __name__ == "__main__":
    print("PART 1")
    print(get_total_points(PATH_TO_FILE))
