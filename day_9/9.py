"""Day 9, part 1 and 2 of Advent Of Code https://adventofcode.com/2021/day/9 """

from typing import List

import numpy as np


def get_input_data(filename: str) -> List[str]:
    with open(filename, "r") as f:
        list_of_lines = f.read().split("\n")
    return list_of_lines


def format_data(data: List[str]) -> np.ndarray:
    return np.array([np.int8(x) for x in "".join(data)])


def part_1(input_data: List[str]) -> int:
    line_length: int = len(input_data[0])
    arr = format_data(input_data)
    arr_length = len(arr)

    min_total: int = 0
    for i, num in enumerate(arr):
        if num == 9:
            continue

        elif i == 0:  # top left corner.
            if (num < arr[i + 1]) and (num < arr[i + line_length]):
                min_total += num + 1

        elif i == line_length - 1:  # top right corner.
            if (num < arr[i - 1]) and (num < arr[i + line_length]):
                min_total += num + 1

        elif i == arr_length - line_length:  # bottom left corner.
            if (num < arr[i + 1]) and (num < arr[i - line_length]):
                min_total += num + 1

        elif i == arr_length - 1:
            if (num < arr[i - 1]) and (num < arr[i - line_length]):
                min_total += num + 1

        elif i < line_length:  # top line
            if (
                (num < arr[i - 1])
                and (num < arr[i + 1])
                and (num < arr[i + line_length])
            ):
                min_total += num + 1

        elif (i + line_length) % line_length == 0:  # left edge
            if (
                (num < arr[i + 1])
                and (num < arr[i + line_length])
                and (num < arr[i - line_length])
            ):
                min_total += num + 1

        elif (i + 1) % line_length == 0:  # right edge
            if (
                (num < arr[i - 1])
                and (num < arr[i + line_length])
                and (num < arr[i - line_length])
            ):
                min_total += num + 1

        elif i > arr_length - line_length - 1:  # bottom line
            if (
                (num < arr[i - 1])
                and (num < arr[i + 1])
                and (num < arr[i - line_length])
            ):
                min_total += num + 1

        else:  # general body.
            if (
                (num < arr[i - 1])
                and (num < arr[i + 1])
                and (num < arr[i + line_length])
                and (num < arr[i - line_length])
            ):
                min_total += num + 1

    return min_total


def main():
    input_data: List[str] = get_input_data("input.txt")
    ans_one: int = part_1(input_data)

    print(ans_one)


if __name__ == "__main__":
    main()
