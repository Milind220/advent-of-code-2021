from typing import List


with open('input.txt', 'r') as f:
    lines: List[str] = f.readlines()

hor: int = 0
depth: int = 0
aim: int = 0

for line in lines:
    line_things: List[str] = line.split()
    magnitude: int = int(line_things[1])
    direction: str = line_things[0]

    if direction == 'forward':
        hor += magnitude
        depth += aim * magnitude
    
    elif direction == 'up':
        aim -= magnitude
    
    else:
        aim += magnitude
    
final_pos: int = hor * depth
print(final_pos)