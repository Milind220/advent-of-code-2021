from typing import List


with open("input.txt", "r") as f:
    numbers: List[float] = list(map(float, f.readlines()))

sum_list: List[float] = []

for i, num in enumerate(numbers):

    if (i > 0) and (i < len(numbers) - 1):
        numsum: float = num + numbers[i - 1] + numbers[i + 1]
        sum_list.append(numsum)

counter: int = 0
prev_num: float = sum_list[0]

for i, num in enumerate(sum_list):
    if num > prev_num:
        counter += 1

    prev_num = num

print(counter)
