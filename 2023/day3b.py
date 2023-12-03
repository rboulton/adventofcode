from tkinter import W


input='''467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..'''

input = open('2023/input3.txt', 'r').read()

grid = input.strip().split('\n')
width = len(grid[0])
height = len(grid)

def find_row_numbers(row, pos):
    result = []
    out = ['.'] * len(row)
    if row[pos].isdigit():
        out[pos] = row[pos]
    for x in range(pos - 1, -1, -1):
        if not row[x].isdigit():
            break
        out[x] = row[x]
    for x in range(pos + 1, len(row)):
        if not row[x].isdigit():
            break
        out[x] = row[x]
    return [int(x) for x in filter(lambda x: x != '', ''.join(out).split('.'))]
 
def find_adjacent_numbers(rownum, colnum):
    results = []
    for i in range(rownum-1, rownum+2):
        results.extend(find_row_numbers(grid[i], colnum))
    return results

gear_ratios = []
for rownum, row in enumerate(grid):
    for colnum, char in enumerate(row):
        if char == '*':
            nums = find_adjacent_numbers(rownum, colnum)
            if len(nums) == 2:
                gear_ratios.append(nums[0] * nums[1])
       
print(sum(gear_ratios))