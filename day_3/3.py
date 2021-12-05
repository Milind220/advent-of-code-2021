from typing import List


def open_file() -> List[str]:
    with open('input.txt', 'r') as f:
        input_data: List[str] = [x.strip('\n') for x in f.readlines()]
    return input_data


# Part 1 functions
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
        else:
            most_common_bits += '0'
    
    return most_common_bits


def get_epsilon_rate(gamma_rate: str) -> str:
    epsilon_rate: str = gamma_rate.replace('0','a').replace('1', '0').replace('a', '1')
    return epsilon_rate


def convert_to_decimal(binary_string: str) -> int:
    return int(binary_string, 2)


# Part 2 functions
def most_common_bit(input_list: List[str], index: int, oxy:bool = False) -> str:
    num_ones: int = 0
    for num in input_list:
        if num[index] == '1':
            num_ones += 1
    
    if num_ones > len(input_list)/2:
        return '1'
    elif (num_ones == len(input_list)/2) and oxy:
        return '1'
    else:
        return '0'


def trim_oxygen_list(input_list: List[str], index: int, bit: str) -> None:
    """Mutates the list directly."""
    while True:
        start = 0
        for i, num in enumerate(input_list):
            if num[index] != bit:
                del input_list[i]
                start += 1
                break

        if len(input_list) == 1:
            break
        if not start:
            break
                

def trim_carbon_dioxide_list(input_list: List[str],
                       index: int,
                       bit: str
                       ) -> None:
    while True:
        start = 0
        for i, num in enumerate(input_list):
            if num[index] == bit:
                del input_list[i]
                start += 1
                break

        if len(input_list) == 1:
            break

        if not start:
            break


# Main functions
def part_1() -> int:
    input: List[str] = open_file()

    gamma_rate: str = most_common_bits(input)
    epsilon_rate: str = get_epsilon_rate(gamma_rate)

    gamma_rate_decimal: int = convert_to_decimal(gamma_rate)
    epsilon_rate_decimal: int = convert_to_decimal(epsilon_rate)

    return gamma_rate_decimal * epsilon_rate_decimal


def part_2() -> int:
    input: List[str] = open_file()

    o2_list: List[str] = input.copy()
    co2_list: List[str] = input.copy()

    for i in range(12):
        check_bit = most_common_bit(o2_list, index = i, oxy = True)
        trim_oxygen_list(o2_list, index = i, bit = check_bit)
        if len(o2_list) == 1:
            break
    
    oxygen_decimal_rating: int = convert_to_decimal(o2_list[0])
    
    for i in range(12):
        check_bit = most_common_bit(co2_list, index = i, oxy = False)
        trim_carbon_dioxide_list(co2_list, index = i, bit = check_bit)
        if len(co2_list) == 1:
            break

    carbon_decimal_rating: int = convert_to_decimal(co2_list[0])

    return carbon_decimal_rating * oxygen_decimal_rating


if __name__ == '__main__':
    print(part_2())