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

all_elems = set()

def split_elems(a):
    return tuple(re.findall('[A-Z][a-z]*', a))

subs = {}
for row in data[:-2]:
    row = row.split(' ')
    out = split_elems(row[2])
    all_elems.update(out)
    subs.setdefault(row[0], []).append(out)

target = split_elems(target)

all_elems.update(target)
no_subs = all_elems.difference(subs.keys())

no_subs = {
    (k, target.count(k)) for k in no_subs
}

def possible(seq):
    if len(seq) > len(target):
        return False
    counts = Counter(seq)
    for k, v in no_subs:
        if counts[k] > v:
            return False
    return True

def gen(vals):
    for e, out in subs.items():
        i = -1
        while True:
            try:
                i = vals.index(e, i + 1)
            except:
                break
            for sub in out:
                yield tuple(vals[:i] + sub + vals[i+1:])

def step(vals_list):
    r = set()
    for vals in vals_list:
        for newvals in gen(vals):
            # print(vals, '->', newvals)
            if possible(newvals):
                r.add(newvals)
    return r

print(subs)
print()
vals_list = (('e',),)
i = 0
while True:
    i += 1
    vals_list = step(vals_list)
    print(i, len(vals_list), max(len(i) for i in vals_list), len(target))
    if target in vals_list:
        break
print(i)
