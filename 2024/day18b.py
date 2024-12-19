import math, os, re, copy
from grid import Grid, Coord
from collections import namedtuple, Counter

data = '''
5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0
'''
g = Grid(width=7, height=7)

data = open(os.path.join(os.path.dirname(__file__), "input18.txt")).read()
g = Grid(width=71, height=71)

data = data.strip()
data = data.split('\n')

g.clear('.')

for row in data:
    row = row.split(',')
    b = Coord(int(row[0]), int(row[1]))
    g.set(b, '#')
    c = Coord(g.width - 1, g.height - 1)
    s = g.connected_same(0, 0)
    if c not in s:
        print(b)
        break
