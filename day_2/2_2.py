with open('input.txt', 'r') as f:
    lines = f.readlines()

hor: int = 0
depth: int = 0
aim: int = 0

for line in lines:
    direction, magnitude = line.split()
    magnitude = int(magnitude)

    if direction == 'forward':
        hor += magnitude
        depth += aim * magnitude
    
    elif direction == 'up':
        aim -= magnitude
    
    else:
        aim += magnitude
    
final_pos: int = hor * depth
print(final_pos)