import math, os, re, copy
from grid import Grid, Coord
from collections import namedtuple, Counter
from itertools import combinations

data = '''
#####
.####
.####
.####
.#.#.
.#...
.....

#####
##.##
.#.##
...##
...#.
...#.
.....

.....
#....
#....
#...#
#.#.#
#.###
#####

.....
.....
#.#..
###..
###.#
###.#
#####

.....
.....
.....
#....
#.#..
#.#.#
#####
'''

data = open(os.path.join(os.path.dirname(__file__), "input25.txt")).read()
data = data.strip()
data = data.split('\n\n')

locks = []
keys = []
height = 7
for chunk in data:
    g = Grid(chunk.split('\n'))
    assert g.height == height
    t = g.get(0, 0)
    heights = []
    for x in range(g.width):
        for y in range(1, g.height):
            if g.get(x, y) != t:
                break
        heights.append(y - 1)
    if t == '#':
        locks.append(heights)
    else:
        assert t == '.'
        heights = [g.height - 2 - h for h in heights]
        keys.append(heights)

def fit(lock, key):
    for h1, h2 in zip(key, lock):
        h = h1 + h2
        if h + 2 > height:
            return False
    return True

count = 0
for lock in locks:
    for key in keys:
        if fit(lock, key):
            print(lock, key)
            count += 1
print(count)
