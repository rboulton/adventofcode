import math, os, re, copy
from grid import Grid, Coord
from collections import namedtuple, Counter

data = '''
p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3
'''
width, height = 11, 7

data = open(os.path.join(os.path.dirname(__file__), "input14.txt")).read()
width, height = 101, 103
data = data.strip()

robots = []
for row in data.split('\n'):
    px, py, vx, vy = map(int, re.match('p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)', row).groups())
    robots.append([px, py, vx, vy])

def move(robots):
    for robot in robots:
        robot[0] = (robot[0] + robot[2]) % width
        robot[1] = (robot[1] + robot[3]) % height

for _ in range(100):
    print(robots)
    move(robots)

mx = (width - 1) / 2
my = (height - 1) / 2
counts = Counter()
for px, py, _, _ in robots:
    if px == mx or py == my:
        continue
    q = (0 if px < mx else 1) + (0 if py < my else 2)
    counts[q] += 1

print(robots)
print(sorted(counts.items()))
total = 1
for v in counts.values():
    total *= v
print(total)
