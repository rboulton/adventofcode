import math, os, re, copy, json
from collections import namedtuple, Counter
from itertools import permutations
from grid import Grid

data = '''
H => HO
H => OH
O => HH

HOH
'''

data = open(os.path.join(os.path.dirname(__file__), "input19.txt")).read()

data = data.strip()
data = data.split('\n')

start = data[-1]
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
print(len(gen(start, subs)))
