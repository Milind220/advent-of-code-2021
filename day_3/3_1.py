with open('input.txt', 'r') as f:
    lines = f.readlines()

num_bits: int = len(lines[0]) - 1
gamma_rate: str = ''
epsilon_rate: str = ''
total_lines: int = len(lines)

for i in range(num_bits): # For the 5 bits in each number.
    num_ones = 0
    for line in lines:
        if line[i] == '1':
            num_ones += 1
    
    if num_ones > total_lines/2: # 1 is the most common bit in that position.
        gamma_rate += '1'
        epsilon_rate += '0'
    else: # 0 is the most common bit in that position.
        gamma_rate += '0'
        epsilon_rate += '1'

dec_gamma_rate = int(gamma_rate, 2)
dec_epsilon_rate = int(epsilon_rate, 2)

power_consumption: int = dec_epsilon_rate * dec_gamma_rate
print(power_consumption)