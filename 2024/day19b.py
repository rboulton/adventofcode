import math, os, re, copy
from grid import Grid, Coord
from collections import namedtuple, Counter

import re2

data = '''
r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb
'''

data = open(os.path.join(os.path.dirname(__file__), "input19.txt")).read()
data = data.strip()
data = data.split('\n')

patterns = data[0].split(', ')
assert not data[1]
designs = data[2:]

e = '^(?:' + '|'.join(f'(?:{p})' for p in patterns) + ')*$'
r = re2.compile(e)

def possible(design):
    m = r.match(design)
    return r.match(design) is not None

memo = Counter()
memo[''] = 1

def ways(design):
    m = memo[design]
    if m: return m
    r = 0
    for p in patterns:
        if design.startswith(p):
            r += ways(design[len(p):])
    memo[design] = r
    return r

print(sum(
    ways(design)
    for design in designs
    if possible(design)
))
