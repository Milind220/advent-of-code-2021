"""Day 6 of Advent of Code 2021, part 1 and 2"""

from typing import List

import numpy as np


def get_input_data(filename: str) -> List[int]:
    with open(filename, 'r') as f:
        data: List[int] = [int(num) for num in f.readline().split(',')]
    return data


# Part 1 functions
def pass_day(fish_list: List[int]) -> List[int]:
    return [num - 1 for num in fish_list]


def reset_fish(fish_list: List[int]) -> List[int]:
    return [6 if x == -1 else x for x in fish_list]


def part_1(array: List[int]) -> int:
    days: int = 80
    for day in range(days):
        array = pass_day(array)
        new_fish: int = array.count(-1)
        array = reset_fish(array)
        if new_fish:
            array.extend([8] * new_fish)
    
    return len(array)

    # Answer for part 1 was 360761.


def part_2(arr: List[int]) -> int:
    fish_arr: np.ndarray = np.array(arr, dtype = np.int8)
    
    days: int = 256
    for day in range(days):
        print(day)
        fish_arr = fish_arr - 1  # pass a single day
        new_fish = np.count_nonzero(fish_arr == -1)
        fish_arr[fish_arr == -1] = np.int8(6)

        if new_fish:
            fish_arr = np.append(fish_arr, 8 * np.ones(new_fish, dtype = np.int8))

    return len(fish_arr)    


def main():
    raw_data: List[int] = get_input_data('test.txt')
    
    #ans_one = part_1(raw_data)
    ans_two = part_2(raw_data)

    #print(ans_one) # 360761
    print(ans_two)


if __name__ == '__main__':
    main()
