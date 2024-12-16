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

data = '''
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
        d = p - n
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

best_cost = min(nodes[(end, d)] for d in dirs)
stack = set()
for d in dirs:
    if nodes[(end, d)] == best_cost:
        stack.add((end, d))

reverse_edges = {}
for k1, dests in edges.items():
    for k2, cost in dests:
        reverse_edges.setdefault(k2, []).append((k1, -cost),)

on_best = set()
while stack:
    newstack = set()
    for k in stack:
        on_best.add(k[0])
        start_cost = nodes[k]
        for k1, cost in reverse_edges[k]:
            if start_cost + cost == nodes[k1]:
                newstack.add(k1)
    stack = newstack
print(g)
for p in on_best:
    g.set(p, 'O')
print(g)
print(len(on_best))
