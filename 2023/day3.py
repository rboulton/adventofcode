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

symbol_positions = {}
for rownum, row in enumerate(grid):
    for colnum, char in enumerate(row):
        if char.isdigit() or char == '.':
            continue
        symbol_positions.setdefault(rownum, []).append(colnum)

part_numbers = []
for rownum, row in enumerate(grid):
    chars = ["."] * len(row)
    for i in range(rownum-1, rownum+2):
        for pos in symbol_positions.get(i, []):
            if row[pos].isdigit():
                chars[pos] = row[pos]
            for x in range(pos - 1, -1, -1):
                if not row[x].isdigit():
                    break
                chars[x] = row[x]
            for x in range(pos + 1, len(row)):
                if not row[x].isdigit():
                    break
                chars[x] = row[x]
    for val in ''.join(chars).split('.'):
        if val == '': continue
        part_numbers.append(int(val))
        
print(sum(part_numbers))