import re
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Final

PATH_TO_FILE: Final[str] = "./Day4/input_file.txt"


@dataclass
class ScratchCardAdministration:
    _number_of_cards: defaultdict[int] = field(
        default_factory=lambda: defaultdict(lambda: 1)
    )

    def get_number_of_cards(self, card_number: int) -> int:
        return self._number_of_cards[card_number]

    def add_cards_for(self, card_number: int, number: int) -> None:
        self._number_of_cards[card_number] += number

    @property
    def number_of_cards(self) -> int:
        return sum(value for value in self._number_of_cards.values())


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


def get_number_of_matching_numbers(card_record: str) -> int:
    return sum(
        1
        for number in get_winning_numbers(card_record)
        if number in get_ticket_numbers(card_record)
    )


def get_total_points(path_to_file: str) -> int:
    with open(path_to_file, "r+") as file:
        score = 0
        for card in file.readlines():
            score += get_points(get_number_of_matching_numbers(card))
    return score


def get_total_number_of_scratch_cards(path_to_file: str) -> int:
    with open(path_to_file, "r+") as file:
        administration = ScratchCardAdministration()
        for card_number, card in enumerate(file.readlines()):
            number_of_cards = administration.get_number_of_cards(card_number)
            number_of_matches = get_number_of_matching_numbers(card)

            next_cards_to_copy = [
                card_number + i for i in range(1, number_of_matches + 1)
            ]
            add_new_cards_for(next_cards_to_copy, number_of_cards, administration)

    return administration.number_of_cards


def add_new_cards_for(
    cards_to_copy: list[int],
    number_of_cards: int,
    card_administration: ScratchCardAdministration,
) -> None:
    for card_id in cards_to_copy:
        card_administration.add_cards_for(card_id, number_of_cards)


if __name__ == "__main__":
    print("PART 1")
    print(get_total_points(PATH_TO_FILE))

    print("PART 2")
    print(get_total_number_of_scratch_cards(PATH_TO_FILE))
