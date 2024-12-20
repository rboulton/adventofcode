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
    print(design, m)
    return r.match(design) is not None

print(sum(
    1 if possible(design) else 0
    for design in designs
))
