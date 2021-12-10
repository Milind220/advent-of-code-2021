"""Day 7, part 1 and 2 of Advent Of Code https://adventofcode.com/2021/day/7 """

from typing import List

import numpy as np


def get_input_data(filename: str) -> List[int]:
    with open(filename, 'r') as f:
        data = [int(x) for x in f.readline().split(',')]
    return data


# Part 1 functions
def part_1(input_list: List[int]) -> int:
    arr = np.array(input_list)
    ideal_position: float = np.median(arr)

    return np.absolute(arr - ideal_position).sum()     # Answer to part 1 is 340987.


def part_2(input_list: List[int]) -> int:
    return 1


# Explicit main
def main():
    input_data: List[int] = get_input_data('input.txt')
    ans_one: int = part_1(input_data)
    ans_two: int = part_2(input_data)

    print(ans_one)
    print(ans_two)


if __name__ == '__main__':
    main()
