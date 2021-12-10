with open("input.txt", "r") as f:
    counter: int = 0
    prev_num: float = float(f.readline())

    for i, line in enumerate(f):
        num = float(line)
        if num > prev_num:
            counter += 1

        prev_num = num

print(counter)
