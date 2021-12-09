"""Day 6 of Advent of Code 2021, part 1 and 2"""

from typing import List

import collections


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
    
    return len(array)

    # Answer for part 1 was 360761.


def part_2(arr: List[int], days: int = 18) -> int:
    tracker: Deque[int] = collections.deque([arr.count(i) for i in range(9)])
    
    for day in range(days):
        print(tracker)
        new_fish = tracker[0]
        tracker.rotate(-1)
        tracker[5] += new_fish
        
    return sum(tracker)


# def solve(data, days):
#     
#     for day in range(days):
#         tracker[(day + 7) % 9] += tracker[day % 9]
#     return sum(tracker)
#     # 26984457539


def main():
    raw_data: List[int] = get_input_data('test.txt')
    
    #ans_one = part_1(raw_data, 80)
    ans_two = part_2(raw_data, 18)

    #print(ans_one) # 360761
    print(ans_two)


if __name__ == '__main__':
    main()
