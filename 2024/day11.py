import math, os, re, copy
from grid import Grid, Coord

data = '''
125 17
'''

data = open(os.path.join(os.path.dirname(__file__), "input11.txt")).read()
data = data.strip().split()

stones = [int(s) for s in data]

def evolve(stone):
    if stone == 0:
        return (1,)
    sstone = str(stone)
    if len(sstone) % 2 == 0:
        m = len(sstone) // 2
        return (
            int(sstone[:m]),
            int(sstone[m:]),
        )
    return (2024 * stone,)

def blink(stonelist):
    out = []
    for stone in stonelist:
        out.extend(evolve(stone))
    return out

for _ in range(25):
    stones = blink(stones)
    print(len(stones))
