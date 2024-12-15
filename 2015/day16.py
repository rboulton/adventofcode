import math, os, re, copy, json
from collections import namedtuple, Counter
from itertools import permutations

target = '''
children: 3
cats: 7
samoyeds: 2
pomeranians: 3
akitas: 0
vizslas: 0
goldfish: 5
trees: 3
cars: 2
perfumes: 1
'''

data = open(os.path.join(os.path.dirname(__file__), "input16.txt")).read()
data = data.strip()
data = data.split('\n')

targets = {}
for t in target.strip().split('\n'):
    print(t)
    a = t.split(': ')
    targets[a[0]] = int(a[1])

for row in data:
    sue, things = row.split(': ', 1)
    r = {}
    no = False
    for thing in things.split(', '):
        k, v = thing.split(': ')
        v = int(v)
        if targets[k] != v:
            no = True
            break
        # print(sue, repr(targets[k]), repr(things), repr(k), repr(v))
    if not no:
        print(sue, things)
