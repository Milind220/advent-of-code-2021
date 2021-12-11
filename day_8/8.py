"""Day 8, part 1 and 2 of Advent Of Code https://adventofcode.com/2021/day/8 """


from typing import Dict, List


def get_input_data(filename: str) -> List[str]:
    with open(filename, "r") as f:
        output = [line.split("|")[1].rstrip("\n") for line in f.readlines()]
    return output


# Part 1 functions
def part_1(data: List[str]) -> int:
    count: Dict = {}
    for x in data:
        for digits in x.split(" "):
            number_of_digits = len(digits)
            if number_of_digits in count:
                count[number_of_digits] += 1
            else:
                count[number_of_digits] = 1

    return count[2] + count[3] + count[4] + count[7]


# Part 2 functions
def check_sub_char(sub: List, sup: List) -> bool:
    return all(x in sup for x in sub)


def char_sub(x: List, y: List) -> List:
    temp = y[:]
    for a in x:
        if a in temp:
            temp.remove(a)
    return temp


def char_add(x: List, y: List) -> List:
    temp = y[:]
    for a in x:
        if a not in temp:
            temp.append(a)
    return sorted(temp)


def part_2() -> int:
    unique: List[str] = [
        x.split("|")[0].rstrip("\n") for x in open("input.txt", "r").readlines()
    ]
    output: List[str] = [
        x.split("|")[1].rstrip("\n") for x in open("input.txt", "r").readlines()
    ]

    result: int = 0

    for i in range(len(unique)):
        encoded = [sorted(x) for x in unique[i].split()]
        decoded: List[str] = [""] * 10
        sorted_output = [sorted(x) for x in output[i].split()]

        # solve simple values
        for x in encoded:
            if len(x) == 2:
                decoded[1] = x
            elif len(x) == 3:
                decoded[7] = x
            elif len(x) == 4:
                decoded[4] = x
            elif len(x) == 7:
                decoded[8] = x

        for x in encoded:
            if len(x) == 5:
                if check_sub_char(decoded[1], x):
                    decoded[3] = x
                elif check_sub_char(char_sub(decoded[1], decoded[4]), x):
                    decoded[5] = x
                else:
                    decoded[2] = x

        decoded[6] = char_add(char_sub(decoded[1], decoded[8]), decoded[5])
        decoded[9] = char_add(decoded[1], decoded[5])
        for x in encoded:
            if x not in decoded:
                decoded[0] = x

        value = ""
        for x in sorted_output:
            value += str(decoded.index(x))
        result += int(value)

    return result


# Explicit main
def main():
    input_data = get_input_data("input.txt")

    ans_one = part_1(input_data)
    ans_two = part_2()

    print(ans_one)
    print(ans_two)


if __name__ == "__main__":
    main()
