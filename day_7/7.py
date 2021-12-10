"""Day 7, part 1 and 2 of Advent Of Code https://adventofcode.com/2021/day/7 """

from typing import List

import numpy as np


def get_input_data(filename: str) -> List[int]:
    with open(filename, "r") as f:
        data = [int(x) for x in f.readline().split(",")]
    return data


# Part 1 functions
def part_1(input_list: List[int]) -> int:
    arr: np.ndarray = np.array(input_list)
    ideal_position: float = np.median(arr)

    return np.absolute(arr - ideal_position).sum()
    # Answer to part 1 is 340987.


# Part 2 functions
def _calculate_fuel(total_steps: int) -> int:
    return np.arange(1, total_steps + 1).sum()


def part_2(input_list: List[int]) -> int:
    arr: np.ndarray = np.array(input_list, dtype=np.int16)

    median: int = int(np.median(arr))
    max: int = int(np.max(arr))

    fuel: int = 3849573485397
    for num in range(0, max + 1):
        steps: int = np.absolute(arr - num).sum()
        new_fuel: int = _calculate_fuel(steps)

        if new_fuel < fuel:
            fuel = new_fuel

    return fuel


# Explicit main
def main():
    input_data: List[int] = get_input_data("test.txt")
    # ans_one: int = part_1(input_data)
    ans_two: int = part_2(input_data)

    # print(ans_one)
    print(ans_two)


if __name__ == "__main__":
    main()
