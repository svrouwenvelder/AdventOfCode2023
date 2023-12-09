import math
import re
from dataclasses import dataclass
from typing import Final

PATH_TO_FILE: Final[str] = "./Day6/input_file.txt"

INITIAL_SPEED: Final[float] = 0.0
ACCELERATION: Final[float] = 1  # mm/ms


@dataclass
class RaceRecord:
    time: int
    distance: int


def load_records(path_to_file: str) -> list[RaceRecord]:
    with open(path_to_file, "r") as f:
        input_data = f.read().splitlines()

    race_durations = [int(ms) for ms in re.findall(r"\d+", input_data[0])]
    record_distances = [int(mm) for mm in re.findall(r"\d+", input_data[1])]
    return [
        RaceRecord(duration, distance)
        for (duration, distance) in zip(race_durations, record_distances)
    ]


def load_as_one_record(path_to_file: str) -> list[RaceRecord]:
    with open(path_to_file, "r") as f:
        input_data = f.read().splitlines()
    return RaceRecord(
        time=extract_on_continuous_number(input_data[0]),
        distance=extract_on_continuous_number(input_data[1]),
    )


def extract_on_continuous_number(record: str) -> int:
    return int("".join(re.findall(r"\d+", record)))


def get_number_of_possibilities_to_beat_record(
    race_record: RaceRecord, min_charge_duration: int = 0
) -> int:
    num_options: int = 0
    chargde_duration: int
    for chargde_duration in range(
        min_charge_duration, race_record.time - min_charge_duration + 1
    ):
        speed: int = chargde_duration * ACCELERATION
        delta_time = race_record.time - chargde_duration
        distance = delta_time * speed
        if distance > race_record.distance:
            num_options += 1
    return num_options


def get_number_of_possibilities_to_beat_races(race_records: list[RaceRecord]) -> int:
    return math.prod(
        get_number_of_possibilities_to_beat_record(record) for record in race_records
    )


if __name__ == "__main__":
    print("PART 1")
    records: list[RaceRecord] = load_records(PATH_TO_FILE)
    print(get_number_of_possibilities_to_beat_races(records))

    print("Part 2")
    record: RaceRecord = load_as_one_record(PATH_TO_FILE)
    print(get_number_of_possibilities_to_beat_record(record, min_charge_duration=14))
