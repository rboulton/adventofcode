import math, os, re, copy
from grid import Grid, Coord
from collections import namedtuple, Counter

data = '''
###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############
'''

data = open(os.path.join(os.path.dirname(__file__), "input20.txt")).read()

data = data.strip()
data = data.split('\n')

g = Grid(data)

s = g.find('S')
e = g.find('E')
print(s, e)
g.set(s, '.')
g.set(e, '.')

def fill_dist(grid, pos):
    result = Grid(data)
    result.clear(None)
    stack = [pos]
    result.set(pos, 0)
    while stack:
        pos = stack.pop()
        dist = result.get(pos)
        for n in g.cartesian_neighbours(pos):
            if grid.get(n) != '.': continue
            d = result.get(n)
            if d is None or dist + 1 < d:
                result.set(n, dist + 1)
                stack.append(n)
    return result


g2 = fill_dist(g, e)
g3 = fill_dist(g, s)

direct = g2.get(s)

c = Counter()
for p in g2.coords(lambda x: x is not None):
    startcost = g2.get(p)
    endcost = g3.get(p)
    if startcost is None: continue
    for n1 in g2.cartesian_neighbours(p):
        for n2 in g2.cartesian_neighbours(n1):
            if g.get(n2) != '.': continue
            if g2.get(n2) == None: continue
            diff = g2.get(n2) - startcost - 2
            diff2 = endcost - g3.get(n2) - 2
            if diff < 100: continue
            if diff != diff2:
                print(diff, diff2)
            else:
                c[diff] += 1

print(sorted(c.items()))
print(sum(c.values()))
