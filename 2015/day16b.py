import math, os, re, copy, json
from collections import namedtuple, Counter
from itertools import permutations

tests = '''
cats > 7
trees > 3
pomeranians < 3
goldfish < 5
children = 3
samoyeds = 2
akitas = 0
vizslas = 0
cars = 2
perfumes = 1
'''.strip().split('\n')
tests = [t.split() for t in tests]
def test(info):
    for k, op, v in tests:
        v = int(v)
        observed = info.get(k)
        if observed is None:
            continue
        observed = int(observed)
        if op == '=':
            if observed != v:
                return False
        if op == '>':
            if observed <= v:
                return False
        if op == '<':
            if observed >= v:
                return False
    return True

data = open(os.path.join(os.path.dirname(__file__), "input16.txt")).read()
data = data.strip()
data = data.split('\n')

for row in data:
    sue, things = row.split(': ', 1)

    info = dict(item.split(': ') for item in things.split(', '))
    if test(info):
        print(sue, things)
