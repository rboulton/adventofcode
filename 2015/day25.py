import sys

def num_from_pos(row, col):
    triangle = row + col - 2
    return (triangle * (triangle + 1)) / 2 + col

def calc_code(num):
    code = 20151125
    while num > 1:
        code = (code * 252533) % 33554393
        num -= 1
    return code


num = num_from_pos(int(sys.argv[1]), int(sys.argv[2]))
print(calc_code(num))
