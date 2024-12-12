import math, os, re, copy
from grid import Grid, Coord

data = '''
89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732
'''

data = open(os.path.join(os.path.dirname(__file__), "input10.txt")).read()
data = data.strip().split('\n')

def find_trails(g, pos, required):
    num = g.get(pos)
    if num != required:
        return set()
    if num == 9:
        return set((pos,))
    r = set()
    for n in g.cartesian_neighbours(pos):
        r.update(find_trails(g, n, num + 1))
    return r

g = Grid(data, int)
r = 0
for trailhead in g.findall(0):
    print(trailhead)
    heads = find_trails(g, trailhead, 0)
    r += len(heads)
    print(len(heads))
    print()
print(r)
