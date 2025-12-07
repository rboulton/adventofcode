import grid
import functools

input = '''123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +  '''

input = open("input6.txt", "r").read()

calcs = {}
for row in input.split('\n'):
    for i, v in enumerate(row.split()):
        calcs.setdefault(i, []).append(v)

total = 0
for calc in calcs.values():
    v = map(int, calc[:-1])
    if calc[-1] == '*':
        r = functools.reduce(lambda x, y: x * y, v)
    else:
        r = functools.reduce(lambda x, y: x + y, v)
    print(r)
    total += r

print(total)
