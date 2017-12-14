import sys

code = [int(line) for line in open(sys.argv[1]).readlines()]

def execute(code):
    position = 0
    step = 0
    while position >= 0 and position < len(code):
        new_pos = position + code[position]
        code[position] += 1
        position = new_pos
        # print position, code
        step += 1
    return step

print(execute(code))