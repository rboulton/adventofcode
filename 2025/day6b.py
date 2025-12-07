import grid
import functools

input = '''123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +  '''

input = open("input6.txt", "r").read()

g = grid.Grid(input.strip('\n').split('\n'))
nums = []
total = 0
for x in range(g.width, -1, -1):
    num = ''.join(
        g.get(x, y) or ' '
        for y in range(g.height - 1)
    ).strip()
    op = g.get(x, g.height - 1)
    if num == '':
        assert len(nums) == 0
        assert op == ' ' or op is None, repr(op)
        continue
    nums.append(int(num))
    if op == '*':
        r = functools.reduce(lambda x, y: x * y, nums)
        print(x, r)
        total += r
        nums = []
    elif op == '+':
        r = functools.reduce(lambda x, y: x + y, nums)
        print(x, r)
        total += r
        nums = []

print(total)
