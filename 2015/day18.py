import math, os, re, copy, json
from collections import namedtuple, Counter
from itertools import permutations
from grid import Grid

data = '''
.#.#.#
...##.
#....#
..#...
#.#..#
####..
'''

data = open(os.path.join(os.path.dirname(__file__), "input18.txt")).read()

data = data.strip()
data = data.split('\n')

def next(g):
    r = copy.deepcopy(g)
    for c in r.coords():
        on = g.get(c) == '#'
        n = sum(
            1 if g.get(nc) == '#' else 0
            for nc in g.all_neighbours(c)
        )
        if on and n != 2 and n != 3:
            # print(f'{c} -> .')
            r.set(c, '.')
        if not on and n == 3:
            # print(f'{c} -> #')
            r.set(c, '#')
    return r

g = Grid(data)

print(g)
for _ in range(100):
    g = next(g)
    print()
    print(g)
print(len(list(g.findall('#'))))
