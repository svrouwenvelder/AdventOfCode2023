from dataclasses import dataclass
from enum import Enum
from typing import ClassVar, Final

PATH_TO_FILE: Final[str] = "./Day7/input_file.txt"


class HandType(int, Enum):
    FIVE_OF_A_KIND = 7
    FOUR_OF_A_KIND = 6
    FULL_HOUSE = 5
    THREE_OF_A_KIND = 4
    TWO_PAIR = 3
    ONE_PAIR = 2
    HIGH_CARD = 1


@dataclass
class Hand:
    hand: str
    bid: int
    type: HandType
    score_order: ClassVar

    def as_int(self) -> tuple:
        return [Hand.score_order.index(card) for card in self.hand]


def determine_hand_type(hand: str, include_joker: bool = False) -> None:
    if include_joker:
        occurance: list[int] = sorted(
            [hand.count(c) for c in set(hand) if c != "J"]
        ) or [0]
        occurance[-1] += hand.count("J")
    else:
        occurance: list[int] = sorted([hand.count(c) for c in set(hand)])

    if 5 in occurance:
        return HandType.FIVE_OF_A_KIND
    if 4 in occurance:
        return HandType.FOUR_OF_A_KIND
    if occurance == [2, 3]:
        return HandType.FULL_HOUSE
    if 3 in occurance:
        return HandType.THREE_OF_A_KIND
    if occurance == [1, 2, 2]:
        return HandType.TWO_PAIR
    if 2 in occurance:
        return HandType.ONE_PAIR
    return HandType.HIGH_CARD


def extract_hands(path_to_file: str, include_jokers: bool = False) -> list[Hand]:
    hands: list[Hand] = []
    for record in open(path_to_file, "r").read().splitlines():
        hand, bid = record.split(" ")
        hand_type = determine_hand_type(hand, include_jokers)
        hands.append(Hand(hand, int(bid), hand_type))
    return hands


def sort_hands_ascending(hands: list[Hand]) -> list[Hand]:
    return sorted(hands, key=lambda hand: (hand.type, hand.as_int()))


def get_total_winnings(hands: list[Hand]) -> int:
    return sum((rank + 1) * hand.bid for rank, hand in enumerate(hands))


if __name__ == "__main__":
    print("PART1")
    Hand.score_order = "23456789TJQKA"
    hands = sort_hands_ascending(extract_hands(PATH_TO_FILE))
    print(get_total_winnings(hands))

    print("PART1")
    Hand.score_order = "J23456789TQKA"
    hands = sort_hands_ascending(extract_hands(PATH_TO_FILE, include_jokers=True))
    print(get_total_winnings(hands))
