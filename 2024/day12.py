import math, os, re, copy
from grid import Grid, Coord

data = '''
RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE
'''

data = open(os.path.join(os.path.dirname(__file__), "input12.txt")).read()
data = data.strip().split('\n')

g = Grid(data)
r = copy.deepcopy(g)

total = 0
for c in g.coords(lambda val: val is not None):
    val = g.get(c)
    region = g.connected_same(c)
    perimeter = 0
    for i in region:
        g.set(i, None)
        for n in r.cartesian_neighbours(i, include_out_of_bounds=True):
            if r.get(n) != val:
                perimeter += 1
    area = len(region)
    print(c, region, area, perimeter)
    total += area * perimeter
print(total)
