# Imports
from typing import List

import numpy as np


def get_data(filename: str) -> List[List[str]]:
    with open(filename, 'r') as f:
        data: List[List[str]] = [
            line.strip('\n').split() for line in f.readlines()
            if line != '\n'
            ]
    return data


# Part 1 function definitions
def format_array(data: List[List[str]]) -> np.ndarray:
    arr = np.array([[int(x) for x in lst] for lst in data])
    reshaped = arr.reshape(int(len(data)/5), 5, 5)
    return reshaped


def eject_num(num: int, array: np.ndarray) -> np.ndarray:
    mod_array = array.copy()
    mod_array[mod_array == num] = 0
    return mod_array


def check_win(matrix_list: np.ndarray) -> int:
    for i, matrix in enumerate(matrix_list):
        # Check row and column win condition.
        for row in matrix:
            if np.sum(row) == 0:
                return i
        
        for col in np.transpose(matrix):
            if np.sum(col) == 0:
                return i
    return -1


def get_matrix_sum(matrix_list: np.ndarray, index: int) -> int:
    return np.sum(matrix_list[index])


# Part 2 function definitions



# Main functions
def part_1() -> None:
    input_data = get_data('input.txt')

    roll_call = [int(num) for num in input_data.pop(0)[0].split(',')]
    original_matrix_list = format_array(input_data)
    matrix_list = original_matrix_list.copy()

    mat_ind = -1
    winning_number = 0
    for i, num in enumerate(roll_call):
        matrix_list = eject_num(num, matrix_list)
        if i > 3: # Index 4 onwards there's a possibility of a matrix having won.

            # Check for winner matrix
            mat_ind = check_win(matrix_list)
            if mat_ind != -1:
                winning_number: int  = num
                break
             
    mat_sum = get_matrix_sum(matrix_list, mat_ind)
    print(mat_sum * winning_number)


def part_2() -> None:
    pass


if __name__ == '__main__':
    part_1()