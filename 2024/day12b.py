import math, os, re, copy
from grid import Grid, Coord

data = '''
AAAAAA
AAABBA
AAABBA
ABBAAA
ABBAAA
AAAAAA
'''

data = '''
EEEEE
EXXXX
EEEEE
EXXXX
EEEEE
'''

data = '''
AAAA
BBCD
BBCC
EEEC
'''

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

# Represent a fence piece by coordinate of the square on the inside, and a
# vector indicating the direction from inside to outside.

total = 0
for c in g.coords(lambda val: val is not None):
    val = g.get(c)
    region = g.connected_same(c)
    fence = {}
    for i in region:
        g.set(i, None)
        for n in r.cartesian_neighbours(i, include_out_of_bounds=True):
            if r.get(n) != val:
                fence.setdefault((n-i), set()).add(i)
    perimeter = 0
    for dir, pieces in fence.items():
        e = Grid(g.rows, lambda _: ' ')
        for piece in pieces:
            e.set(piece, '.')

        # print(dir)
        while dir != Coord(0, -1):
            dir = dir.rotate_right()
            e = e.rotate_right()
        # print(dir)
        # print(e)
        prev = Coord(-100, -100)
        for c in e.coords(lambda v: v == '.'):
            if c - prev != Coord(1, 0):
                # print(c, c - prev)
                perimeter += 1
            prev = c
    area = len(region)
    # print(c, region, area, perimeter)
    print(c, area, perimeter)
    total += area * perimeter
print(total)
