with open('input.txt', 'r') as f:
    lines = f.readlines()

hor_pos: int = 0
depth_pos: int = 0

for line in lines:
    direction, magnitude = line.split()
    magnitude = int(magnitude)

    if direction == 'forward':
        hor_pos += magnitude
    
    elif direction == 'up':
        depth_pos -= magnitude
    
    else:
        depth_pos += magnitude
    
final_pos: int = hor_pos * depth_pos
print(final_pos)