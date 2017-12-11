# Use cube coordinates, as defined here:
# https://www.redblobgames.com/grids/hexagons/

import sys

moves = open(sys.argv[1]).read().strip().split(',')

dirs = {
    'n': (0, 1, -1),
    'ne': (1, 0, -1),
    'se': (1, -1, 0),
    's': (0, -1, 1),
    'sw': (-1, 0, 1),
    'nw': (-1, 1, 0),
}

coord = [0, 0, 0]
maxdist = 0

def dist(a):
    return (abs(a[0]) + abs(a[1]) + abs(a[2])) / 2

for move in moves:
    d = dirs[move]
    coord[0] += d[0]
    coord[1] += d[1]
    coord[2] += d[2]
    maxdist = max(maxdist, dist(coord))

print(dist(coord))
print(maxdist)
