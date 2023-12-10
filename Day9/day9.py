import re
from typing import Final

import numpy as np
from numpy.typing import NDArray

PATH_TO_FILE: Final[str] = "./Day9/input_file.txt"


def extract_numbers(record: str) -> list[int]:
    return [int(i) for i in re.findall(r"-\d+|\d+", record)]


def predict_forwards(numbers: list[int]) -> int:
    delta = 0
    for diff in reversed(_get_differences(numbers)):
        delta = diff[-1] + delta
    return numbers[-1] + delta


def predict_backwards(numbers: list[int]) -> int:
    delta = 0
    for diff in reversed(_get_differences(numbers)):
        delta = diff[0] - delta
    return numbers[0] - delta


def _get_differences(numbers: list[int]) -> list[NDArray[np.int32]]:
    deltas: list[NDArray[np.int32]] = [np.diff(numbers)]
    while deltas[-1].size != 1 and not np.allclose(deltas[-1], 0):
        deltas.append(np.diff(deltas[-1]))
    return deltas


def get_summed_prediction(path_to_file: str, prediction) -> int:
    data = open(path_to_file, "r").read().rstrip().splitlines()
    return sum(prediction(extract_numbers(numbers)) for numbers in data)


if __name__ == "__main__":
    print("PART 1")
    print(get_summed_prediction(PATH_TO_FILE, predict_forwards))

    print("PART 2")
    print(get_summed_prediction(PATH_TO_FILE, predict_backwards))
