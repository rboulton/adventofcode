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
limit = 50

data = open(os.path.join(os.path.dirname(__file__), "input20.txt")).read()
limit = 100

cheatdist = 20

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

def walk_upto(startpos, steps):
    visited = set()
    stack = [startpos]
    for s in range(1, steps + 1):
        newstack = []
        for p in stack:
            for n in g.cartesian_neighbours(p):
                if n in visited: continue
                visited.add(n)
                newstack.append(n)
                yield n, s
        stack = newstack

c = Counter()
for p in g2.coords(lambda x: x is not None):
    startcost = g2.get(p)
    endcost = g3.get(p)
    if startcost is None: continue
    for n2, steps in walk_upto(p, cheatdist):
        if g.get(n2) != '.': continue
        if g2.get(n2) == None: continue
        diff = g2.get(n2) - startcost - steps
        diff2 = endcost - g3.get(n2) - steps
        assert diff == diff2
        # print(n2, diff)
        if diff < limit: continue
        c[diff] += 1

print(sorted(c.items()))
print(sum(c.values()))
