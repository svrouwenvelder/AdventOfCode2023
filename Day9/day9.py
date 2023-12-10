import re
from typing import Final
import numpy as np
from numpy.typing import NDArray

PATH_TO_FILE: Final[str] = "./Day9/input_file.txt"
PATH_TO_TEST_FILE: Final[str] = "./Day9/test_file.txt"

def extract_numbers(record: str) -> list[int]:
    return [int(i) for i in re.findall(r'-\d+|\d+', record)]

def predict(numbers: list[int]) -> int:
    deltas: list[NDArray[np.int32]] = [np.diff(numbers)]
    while deltas[-1].size != 1 and not np.allclose(deltas[-1], 0):
        deltas.append(np.diff(deltas[-1]))

    delta = 0
    for diff in reversed(deltas):
        delta = diff[-1] + delta
    return numbers[-1] + delta


def get_summed_prediction(path_to_file: str) -> int:
    data = open(path_to_file, 'r').read().rstrip().splitlines()
    return sum(predict(extract_numbers(numbers)) for numbers in data)

if __name__ == "__main__":
    print("PART 1")
    print(get_summed_prediction(PATH_TO_FILE))