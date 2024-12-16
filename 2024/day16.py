import math, os, re, copy
from grid import Grid, Coord
from collections import namedtuple, Counter

data = '''
###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############
'''

data_ = '''
#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################
'''

data = open(os.path.join(os.path.dirname(__file__), "input16.txt")).read()
data = data.strip()

g = Grid(data.split('\n'))

start = g.find('S')
end = g.find('E')
g.set(start, '.')
g.set(end, '.')

east = Coord(1, 0)
dirs = (
    east,
    east.rotate_right(),
    east.rotate_right().rotate_right(),
    east.rotate_right().rotate_right().rotate_right(),
)

edges = {}
for p in g.findall('.'):
    for d in dirs:
        d1 = d.rotate_right()
        edges.setdefault((p, d), []).append(((p, d1), 1000))
        edges.setdefault((p, d1), []).append(((p, d), 1000))

    for n in g.cartesian_neighbours(p):
        if g.get(n) != '.':
            continue
        d = n - p
        edges.setdefault((p, d), []).append(((n, d), 1))

stack = set(((start, east),))
nodes = {(start, east): 0}
while stack:
    newstack = set()
    for k in stack:
        start_cost = nodes.get(k)
        for k1, cost in edges[k]:
            old = nodes.get(k1)
            if old is None or old > start_cost + cost:
                nodes[k1] = start_cost + cost
                newstack.add(k1)
    stack = newstack



print(len(nodes))
print(len(edges))
print(min(nodes[(end, d)] for d in dirs))
