"""Day 5, part 1 and 2 of Advent Of Code https://adventofcode.com/2021/day/5 """

from typing import Dict, List, Tuple


def get_input_data(filename: str) -> List[List[int]]:
    d = [[int(x) for x in l.replace(" -> ", " ").replace(",", " ").split()] for l in open(filename,'rt')]
    return d


def main() -> None:
    """Single Explicit Main for both parts 1 and 2"""
    d: List[List[int]] = get_input_data('input.txt')

    a: Dict[Tuple[int, int], int] = {}
    b: Dict[Tuple[int, int], int] = {}

    for x1, y1, x2, y2 in d:
        if x1 == x2:
            if y1 > y2:
                y1, y2 = y2, y1
            for y in range(y1, y2 + 1):
                a[(x1, y)] = a.get((x1, y), 0) + 1
                b[(x1, y)] = b.get((x1, y), 0) + 1

        elif y1 == y2:
            if x1 > x2:
                x1, x2 = x2, x1
            for x in range(x1, x2 + 1):
                a[(x, y1)] = a.get((x, y1), 0) + 1
                b[(x, y1)] = b.get((x, y1), 0) + 1

        else:
            if x1 > x2:
                x1, x2, y1, y2 = x2, x1, y2, y1

            for x in range(x1, x2 + 1):
                if y2 > y1:
                    y = y1 + (x - x1)
                else:     
                    y = y1 - (x - x1)

                b[(x, y)] = b.get((x, y), 0) + 1
    
    part_one_answer: int = sum(v > 1 for v in a.values())
    part_two_answer: int = sum(v > 1 for v in b.values())

    print(f'Part 1: {part_one_answer}\nPart 2: {part_two_answer}')


if __name__ == '__main__':
    main()
