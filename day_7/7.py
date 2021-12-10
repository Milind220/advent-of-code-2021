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
def _calculate_total_fuel(arr: np.ndarray):
    steps_list: List[int] = arr.tolist()
    total_fuel: int = int(
        np.array([np.arange(1, x + 1, dtype=int).sum() for x in steps_list]).sum()
    )
    return total_fuel


def part_2(input_list: List[int]) -> int:
    arr: np.ndarray = np.array(input_list, dtype=np.int16)

    mean: int = int(np.mean(arr))

    fuel: int = 100000000000000  # Random very large number.
    for num in range(mean - 5, mean + 5):
        steps_arr: np.ndarray = np.absolute(arr - num)
        new_fuel: int = _calculate_total_fuel(steps_arr)

        if new_fuel < fuel:
            fuel = new_fuel

    return fuel
    # Answer to part 2 is 96987874.


# Explicit main
def main():
    input_data: List[int] = get_input_data("input.txt")
    ans_one: int = part_1(input_data)
    ans_two: int = part_2(input_data)

    print(ans_one)
    print(ans_two)


if __name__ == "__main__":
    main()
