from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Final

PATH_TO_FILE: Final[str] = "./Day5/input_file.txt"
PATH_TO_TEST_FILE: Final[str] = "./Day5/test_file.txt"


@dataclass
class Almanac:
    seed2soil: ResourceMap
    soil2fertilizer: ResourceMap
    fertilizer2water: ResourceMap
    water2light: ResourceMap
    light2temperature: ResourceMap
    temperature2humidity: ResourceMap
    humidity2location: ResourceMap

    def get_location(self, seed_nr: int) -> int:
        soil = self.seed2soil.map(seed_nr)
        fertilizer = self.soil2fertilizer.map(soil)
        water = self.fertilizer2water.map(fertilizer)
        light = self.water2light.map(water)
        temperature = self.light2temperature.map(light)
        humidity = self.temperature2humidity.map(temperature)
        return self.humidity2location.map(humidity)


@dataclass
class ResourceMap:
    _records: list[ResourceRecord] = field(default_factory=list)

    def map(self, resource_id: int) -> int:
        for record in self._records:
            if record.contains(resource_id):
                return record.map(resource_id)
        return resource_id


@dataclass
class ResourceRecord:
    destination_start: int
    source_start: int
    length: int

    def contains(self, source_id: int) -> bool:
        start = self.source_start
        stop = self.source_start + self.length - 1
        return start <= source_id <= stop

    def map(self, source_id: int) -> int:
        offset = source_id - self.source_start
        return self.destination_start + offset


def _extract_numbers(record: str) -> list[int]:
    numbers = re.findall(r"\d+", record)
    return [int(n) for n in numbers]


def create_resource_mapping(values: list[int]) -> ResourceMap:
    records: list[ResourceRecord] = []
    for i in range(0, len(values), 3):
        records.append(ResourceRecord(values[i], values[i + 1], values[i + 2]))
    return ResourceMap(records)


def process_almanac(path_to_file: str) -> tuple[list[int], Almanac]:
    data: list[str] = open(path_to_file, "r+").read().split("\n\n")
    seeds: list[int] = _extract_numbers(data[0])

    seed2soil = create_resource_mapping(_extract_numbers(data[1]))
    soil2fertilizer = create_resource_mapping(_extract_numbers(data[2]))
    fertilizer2water = create_resource_mapping(_extract_numbers(data[3]))
    water2light = create_resource_mapping(_extract_numbers(data[4]))
    light2temperature = create_resource_mapping(_extract_numbers(data[5]))
    temperature2humidity = create_resource_mapping(_extract_numbers(data[6]))
    humidity2location = create_resource_mapping(_extract_numbers(data[7]))
    return seeds, Almanac(
        seed2soil,
        soil2fertilizer,
        fertilizer2water,
        water2light,
        light2temperature,
        temperature2humidity,
        humidity2location,
    )


def get_lowest_location_number(seeds: list[int], almanac: Almanac) -> int:
    return min(almanac.get_location(seed) for seed in seeds)


def get_lowest_location_number_with_ranges(
    seed_start: int, seed_stop: int, almanac: Almanac
) -> int:
    return min(
        almanac.get_location(seed) for seed in range(seed_start, seed_start + seed_stop)
    )


if __name__ == "__main__":
    print("PART1")
    seeds, almanac = process_almanac(PATH_TO_FILE)
    print(get_lowest_location_number(seeds, almanac))

    print("PART2")
    # WIP: requires interval math rather than brute forcing
    print(
        min(
            get_lowest_location_number_with_ranges(seeds[i], seeds[i + 1], almanac)
            for i in range(0, len(seeds), 2)
        )
    )
