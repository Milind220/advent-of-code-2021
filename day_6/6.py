"""Day 6 of Advent of Code 2021, part 1 and 2"""

from typing import List

import collections


# Type definition
Deque = collections.deque


def get_input_data(filename: str) -> List[int]:
    with open(filename, 'r') as f:
        data: List[int] = [int(num) for num in f.readline().split(',')]
    return data


# Part 1 functions
def pass_day(fish_list: List[int]) -> List[int]:
    return [num - 1 for num in fish_list]


def reset_fish(fish_list: List[int]) -> List[int]:
    return [6 if x == -1 else x for x in fish_list]


def part_1(array: List[int], days: int = 18) -> int:
    for day in range(days):
        array = pass_day(array)
        new_fish: int = array.count(-1)
        array = reset_fish(array)
        if new_fish:
            array.extend([8] * new_fish)
    
    return len(array)     # Answer for part 1 was 360761.


# Part 2 functions
def part_2(arr: List[int], days: int = 18) -> int:
    tracker: Deque[int] = collections.deque([arr.count(i) for i in range(9)])

    for day in range(days):
        new_fish: int = 0
        new_fish += tracker[0]
        tracker.rotate(-1)
        tracker[6] += new_fish
        
    return sum(tracker)     # Answer for part 2 was 1632779838045.


# Explicit main
def main():
    raw_data: List[int] = get_input_data('input.txt')
    
    ans_one: int = part_1(raw_data, 80)
    ans_two: int = part_2(raw_data, 256)

    print(ans_one) # 360761
    print(ans_two) # 1632779838045


if __name__ == '__main__':
    main()
