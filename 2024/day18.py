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
iterations = 12

data = open(os.path.join(os.path.dirname(__file__), "input18.txt")).read()
g = Grid(width=71, height=71)
iterations = 1024

data = data.strip()
data = data.split('\n')

g.clear('.')

for row in data[:iterations]:
    row = row.split(',')
    b = Coord(int(row[0]), int(row[1]))
    g.set(b, '#')

g2 = Grid(width=g.width, height=g.height)
i = 0
g2.set(0, 0, i)
while g2.get(g2.width - 1, g2.height - 1) is None:
    for e in g2.findall(i):
        for n in g2.cartesian_neighbours(e):
            if g.get(n) == '.' and g2.get(n) is None:
                g2.set(n, i + 1)
    i += 1
    #print(g2)
    #print()

print(g2.get(g2.width - 1, g2.height - 1))
