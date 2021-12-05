from typing import List

def open_file() -> List[str]:
    with open('input.txt', 'r') as f:
        input_data: List[str] = [x.strip('\n') for x in f.readlines()]
    return input_data


def most_common_bits(input_list: List[str], strong_one: bool = False) -> str:

    most_common_bits: str = ''
    num_digits: int = len(input_list[0])

    for index in range(num_digits):  # Loops through the digits.
        
        num_ones: int = 0
        # Now, for the most common bit in each position.
        for num in input_list: 
            if num[index] == '1':
                num_ones += 1
        
        # Add it to the most common bits.
        if num_ones > len(input_list)/2: 
            most_common_bits += '1'
        elif (num_ones == len(input_list)/2) and strong_one:
            most_common_bits += '1'
        else:
            most_common_bits += '0'
    
    return most_common_bits


def get_epsilon_rate(gamma_rate: str) -> str:

    epsilon_rate: str = gamma_rate.replace('0','a').replace('1', '0').replace('a', '1')
    return epsilon_rate


def convert_to_decimal(binary_string: str) -> int:
    return int(binary_string, 2)


def part_1() -> int:
    input: List[str] = open_file()

    gamma_rate: str = most_common_bits(input)
    epsilon_rate: str = get_epsilon_rate(gamma_rate)

    gamma_rate_decimal: int = convert_to_decimal(gamma_rate)
    epsilon_rate_decimal: int = convert_to_decimal(epsilon_rate)

    return gamma_rate_decimal * epsilon_rate_decimal


def part_2() -> int:

    return 1


if __name__ == '__main__':
    pass