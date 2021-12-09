"""Day 6 of Advent of Code 2021, part 1 and 2"""

from typing import List


def get_input_data(filename: str) -> List[int]:
    with open(filename, 'r') as f:
        data: List[int] = [int(num) for num in f.readline().split(',')]
    return data


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


def part_2(array: List[int]) -> int:

    return 1


def main():
    raw_data: List[int] = get_input_data('input.txt')
    ans_two = part_2(raw_data)
    #ans_one = part_1(raw_data)

    #print(ans_one) # 360761
    print(ans_two)


if __name__ == '__main__':
    main()
