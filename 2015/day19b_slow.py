import math, os, re, copy, json
from collections import namedtuple, Counter
from itertools import permutations
from grid import Grid

data = '''
e => H
e => O
H => HO
H => OH
O => HH

HOHOHO
'''

data = open(os.path.join(os.path.dirname(__file__), "input19.txt")).read()

data = data.strip()
data = data.split('\n')

target = data[-1]
start = 'e'

subs = []
for row in data[:-2]:
    row = row.split(' ')
    subs.append((row[0], row[2]))

def gen(start, subs):
    r = set()
    for a, b in subs:
        i = -1
        while True:
            i = start.find(a, i + 1)
            if i < 0:
                break
            r.add(start[:i] + b + start[i+len(a):])
    return r

print(start, subs)
mols = set((start,))
for i in range(1, 1000):
    next_mols = set()
    for mol in mols:
        next_mols.update(gen(mol, subs))
    mols = next_mols
    print(i, mols)
    if target in mols:
        break
print(i)
